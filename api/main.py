from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import datetime
import json
from collections import deque

# ==============================
# App Setup
# ==============================

app = FastAPI(title="AI Intrusion Detection API", version="3.0")

MODEL_PATH = "../model/brute_force_model.pkl"
BLACKLIST_PATH = "../security/blacklist.json"
IP_ACTIVITY_PATH = "../security/ip_activity.json"

os.makedirs("../security", exist_ok=True)

# ==============================
# Configuration
# ==============================

TIME_WINDOW_SECONDS = 60
MAX_REQUESTS_PER_WINDOW = 10
BLACKLIST_LIMIT = 5
TEMP_BAN_MINUTES = 2

# ==============================
# Load Model
# ==============================

try:
    model = joblib.load(MODEL_PATH)
except:
    model = None

# ==============================
# Schema
# ==============================

class LoginAttempt(BaseModel):
    ip_address: str
    failed_attempts: int
    time_between_attempts: float
    login_success: int
    ip_attempts: int

# ==============================
# Utility
# ==============================

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def calculate_risk_score(ml_probability, request_rate, failure_ratio):
    score = (ml_probability * 0.6) + (request_rate * 0.2) + (failure_ratio * 0.2)
    return round(score * 100, 2)

# ==============================
# Rate Limiting + Time Window
# ==============================

def update_ip_activity(ip, attack_detected):

    ip_data = load_json(IP_ACTIVITY_PATH)
    now = datetime.datetime.now()

    if ip not in ip_data:
        ip_data[ip] = {
            "timestamps": [],
            "attack_count": 0,
            "banned_until": None
        }

    # Remove old timestamps outside window
    ip_data[ip]["timestamps"] = [
        t for t in ip_data[ip]["timestamps"]
        if (now - datetime.datetime.fromisoformat(t)).seconds <= TIME_WINDOW_SECONDS
    ]

    # Add current timestamp
    ip_data[ip]["timestamps"].append(now.isoformat())

    if attack_detected:
        ip_data[ip]["attack_count"] += 1

    save_json(IP_ACTIVITY_PATH, ip_data)

    return ip_data[ip]

# ==============================
# Blacklist + Temp Ban
# ==============================

def check_blacklist(ip_data, ip):

    now = datetime.datetime.now()

    # Check temp ban
    if ip_data["banned_until"]:
        banned_until = datetime.datetime.fromisoformat(ip_data["banned_until"])
        if now < banned_until:
            return "TEMP_BANNED"

    # Permanent blacklist
    blacklist = load_json(BLACKLIST_PATH)
    if ip in blacklist:
        return "BLACKLISTED"

    return None


def apply_temp_ban(ip):

    ip_data = load_json(IP_ACTIVITY_PATH)
    now = datetime.datetime.now()

    ip_data[ip]["banned_until"] = (
        now + datetime.timedelta(minutes=TEMP_BAN_MINUTES)
    ).isoformat()

    save_json(IP_ACTIVITY_PATH, ip_data)

# ==============================
# Routes
# ==============================

@app.post("/predict")
def predict(login: LoginAttempt):

    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")

    ip_data = update_ip_activity(login.ip_address, False)

    blacklist_status = check_blacklist(ip_data, login.ip_address)
    if blacklist_status:
        return {"status": blacklist_status}

    features = [[
        login.failed_attempts,
        login.time_between_attempts,
        login.login_success,
        login.ip_attempts
    ]]

    prediction = model.predict(features)[0]
    ml_prob = model.predict_proba(features)[0][1]

    attack_detected = True if prediction == 1 else False

    ip_data = update_ip_activity(login.ip_address, attack_detected)

    request_rate = min(len(ip_data["timestamps"]) / MAX_REQUESTS_PER_WINDOW, 1)
    failure_ratio = min(login.failed_attempts / 20, 1)

    risk_score = calculate_risk_score(ml_prob, request_rate, failure_ratio)

    # Automatic temp ban
    if request_rate >= 1 or ip_data["attack_count"] >= BLACKLIST_LIMIT:
        apply_temp_ban(login.ip_address)
        return {
            "status": "TEMP_BANNED",
            "reason": "Too many requests or repeated attacks"
        }

    return {
        "prediction": "ATTACK" if attack_detected else "NORMAL",
        "risk_score_percent": risk_score,
        "requests_in_window": len(ip_data["timestamps"]),
        "attack_count": ip_data["attack_count"]
    }


@app.get("/blacklist")
def view_blacklist():
    return load_json(BLACKLIST_PATH)

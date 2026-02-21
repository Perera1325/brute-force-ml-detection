from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import datetime
import json

# ==============================
# App Setup
# ==============================

app = FastAPI(
    title="AI Brute Force Detection API",
    version="2.0"
)

MODEL_PATH = "../model/brute_force_model.pkl"
BLACKLIST_PATH = "../security/blacklist.json"
IP_ACTIVITY_PATH = "../security/ip_activity.json"

os.makedirs("../security", exist_ok=True)

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
# Utility Functions
# ==============================

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def calculate_risk_score(prob):
    return round(prob * 100, 2)


# ==============================
# Campaign Detection Logic
# ==============================

ATTACK_THRESHOLD = 3
BLACKLIST_LIMIT = 5


def update_ip_activity(ip, attack_detected):

    ip_data = load_json(IP_ACTIVITY_PATH)

    if ip not in ip_data:
        ip_data[ip] = {
            "total_requests": 0,
            "attack_count": 0
        }

    ip_data[ip]["total_requests"] += 1

    if attack_detected:
        ip_data[ip]["attack_count"] += 1

    save_json(IP_ACTIVITY_PATH, ip_data)

    return ip_data[ip]


def check_and_blacklist(ip, attack_count):

    blacklist = load_json(BLACKLIST_PATH)

    if attack_count >= BLACKLIST_LIMIT:
        blacklist[ip] = {
            "blacklisted_at": str(datetime.datetime.now()),
            "reason": "Multiple brute force attempts"
        }

        save_json(BLACKLIST_PATH, blacklist)
        return True

    return False


# ==============================
# Routes
# ==============================

@app.get("/")
def home():
    return {"status": "running", "version": "2.0"}


@app.get("/blacklist")
def view_blacklist():
    return load_json(BLACKLIST_PATH)


@app.post("/clear_blacklist")
def clear_blacklist():
    save_json(BLACKLIST_PATH, {})
    return {"message": "Blacklist cleared"}


@app.post("/predict")
def predict(login: LoginAttempt):

    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")

    blacklist = load_json(BLACKLIST_PATH)

    if login.ip_address in blacklist:
        return {
            "prediction": "BLOCKED",
            "reason": "IP is blacklisted"
        }

    features = [[
        login.failed_attempts,
        login.time_between_attempts,
        login.login_success,
        login.ip_attempts
    ]]

    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0][1]
    risk_score = calculate_risk_score(probability)

    attack_detected = True if prediction == 1 else False

    ip_stats = update_ip_activity(login.ip_address, attack_detected)

    blacklisted = check_and_blacklist(
        login.ip_address,
        ip_stats["attack_count"]
    )

    if blacklisted:
        return {
            "prediction": "BLACKLISTED",
            "message": "IP automatically blacklisted due to repeated attacks"
        }

    return {
        "prediction": "ATTACK" if attack_detected else "NORMAL",
        "risk_score_percent": risk_score,
        "ip_statistics": ip_stats
    }

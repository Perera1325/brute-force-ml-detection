from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
import datetime

# ==============================
# App Initialization
# ==============================

app = FastAPI(
    title="AI Brute Force Detection API",
    description="Machine Learning Powered Intrusion Detection System",
    version="1.0"
)

# ==============================
# Paths
# ==============================

MODEL_PATH = "../model/brute_force_model.pkl"
LOG_FILE = "logs/api_detection_log.txt"

os.makedirs("logs", exist_ok=True)

# ==============================
# Load Model
# ==============================

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print("Error loading model:", e)
    model = None


# ==============================
# Request Schema
# ==============================

class LoginAttempt(BaseModel):
    failed_attempts: int
    time_between_attempts: float
    login_success: int
    ip_attempts: int


# ==============================
# Utility Functions
# ==============================

def calculate_risk_score(probability):
    return round(probability * 100, 2)


def log_api_event(data, prediction, risk_score):
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now()
        f.write(
            f"{timestamp} | "
            f"Data: {data} | "
            f"Prediction: {prediction} | "
            f"Risk Score: {risk_score}%\n"
        )


# ==============================
# Routes
# ==============================

@app.get("/")
def home():
    return {
        "status": "running",
        "message": "Brute Force Detection API is active"
    }


@app.get("/health")
def health_check():
    if model:
        return {"status": "healthy"}
    return {"status": "model_not_loaded"}


@app.post("/predict")
def predict(login: LoginAttempt):

    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        features = [[
            login.failed_attempts,
            login.time_between_attempts,
            login.login_success,
            login.ip_attempts
        ]]

        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]
        risk_score = calculate_risk_score(probability)

        result = "ATTACK" if prediction == 1 else "NORMAL"

        log_api_event(login.dict(), result, risk_score)

        return {
            "prediction": result,
            "risk_score_percent": risk_score,
            "recommendation":
                "Block IP immediately" if result == "ATTACK"
                else "Allow access"
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

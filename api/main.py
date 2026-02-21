from fastapi import FastAPI
import joblib

app = FastAPI()

model = joblib.load("../model/brute_force_model.pkl")


@app.get("/")
def home():
    return {"message": "Brute Force Detection API Running"}


@app.post("/predict")
def predict(
    failed_attempts: int,
    time_between_attempts: float,
    login_success: int,
    ip_attempts: int
):

    features = [[
        failed_attempts,
        time_between_attempts,
        login_success,
        ip_attempts
    ]]

    prediction = model.predict(features)[0]

    if prediction == 1:
        return {"prediction": "Attack"}
    else:
        return {"prediction": "Normal"}

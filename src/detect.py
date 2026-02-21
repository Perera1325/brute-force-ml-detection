import joblib
import numpy as np

model = joblib.load("../model/brute_force_model.pkl")

def detect_attack(features):

    prediction = model.predict([features])[0]

    if prediction == 1:
        return "🚨 Brute Force Attack Detected"
    else:
        return "✅ Normal Activity"


if __name__ == "__main__":

    sample = [15, 0.5, 0, 30]

    result = detect_attack(sample)

    print(result)

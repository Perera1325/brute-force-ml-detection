import joblib
import random
import time
import datetime
import os

# ==============================
# Load Trained Model
# ==============================

MODEL_PATH = "../model/brute_force_model.pkl"
LOG_FILE = "../logs/realtime_monitor_log.txt"

# Ensure log directory exists
os.makedirs("../logs", exist_ok=True)

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    print("❌ Error loading model:", e)
    print("Make sure you trained the model first (run train_model.py)")
    exit()

# ==============================
# Global Counters
# ==============================

attack_count = 0
normal_count = 0
ALERT_THRESHOLD = 5


# ==============================
# Logging Function
# ==============================

def log_event(features, prediction, risk_score):
    try:
        with open(LOG_FILE, "a") as f:
            timestamp = datetime.datetime.now()
            f.write(
                f"{timestamp} | "
                f"Features: {features} | "
                f"Prediction: {prediction} | "
                f"Risk Score: {risk_score}%\n"
            )
    except Exception as e:
        print("⚠️ Logging error:", e)


# ==============================
# Simulated Login Generator
# ==============================

def generate_random_login():
    """
    Simulates real-world login attempts
    """

    # 70% Normal Traffic
    if random.random() < 0.7:
        failed_attempts = random.randint(0, 5)
        time_between = round(random.uniform(5, 60), 2)
        login_success = random.choice([0, 1])
        ip_attempts = random.randint(1, 10)

    # 30% Suspicious Traffic
    else:
        failed_attempts = random.randint(10, 20)
        time_between = round(random.uniform(0.1, 1), 2)
        login_success = 0
        ip_attempts = random.randint(20, 50)

    return [failed_attempts, time_between, login_success, ip_attempts]


# ==============================
# Risk Score Calculation
# ==============================

def calculate_risk_score(probability):
    return round(probability * 100, 2)


# ==============================
# Monitoring Engine
# ==============================

def monitor_system():

    global attack_count
    global normal_count

    print("\n🔐 Real-Time Brute Force Monitoring Started...\n")
    print("Press CTRL + C to stop.\n")

    while True:

        try:
            features = generate_random_login()

            prediction = model.predict([features])[0]
            probability = model.predict_proba([features])[0][1]

            risk_score = calculate_risk_score(probability)

            if prediction == 1:
                attack_count += 1
                print(f"[ALERT] 🚨 Attack Detected | Risk Score: {risk_score}%")

                if attack_count >= ALERT_THRESHOLD:
                    print("\n🔥🔥🔥 MULTIPLE ATTACKS DETECTED — POSSIBLE BRUTE FORCE CAMPAIGN 🔥🔥🔥\n")

            else:
                normal_count += 1
                print(f"[INFO] Normal Activity | Risk Score: {risk_score}%")

            log_event(features, prediction, risk_score)

            print(f"Total Normal: {normal_count} | Total Attacks: {attack_count}")
            print("-" * 60)

            time.sleep(2)

        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped by user.")
            break

        except Exception as e:
            print("⚠️ Runtime error:", e)


# ==============================
# Main Execution
# ==============================

if __name__ == "__main__":
    monitor_system()

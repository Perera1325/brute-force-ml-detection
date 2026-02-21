import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_data(num_samples=1000):
    data = []

    for _ in range(num_samples):

        failed_attempts = np.random.randint(0, 20)
        time_between = np.random.uniform(0.1, 60)
        login_success = np.random.choice([0, 1], p=[0.7, 0.3])
        ip_attempts = np.random.randint(1, 50)

        # Label logic
        if failed_attempts > 10 or time_between < 1:
            label = 1  # attack
        else:
            label = 0  # normal

        data.append([
            failed_attempts,
            time_between,
            login_success,
            ip_attempts,
            label
        ])

    columns = [
        "failed_attempts",
        "time_between_attempts",
        "login_success",
        "ip_attempts",
        "label"
    ]

    df = pd.DataFrame(data, columns=columns)
    return df


if __name__ == "__main__":
    df = generate_data(2000)
    df.to_csv("../data/login_data.csv", index=False)
    print("Dataset saved to data/login_data.csv")

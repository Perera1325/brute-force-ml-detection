import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# =========================
# Load Dataset
# =========================

data = pd.read_csv("../data/login_data.csv")

X = data.drop("label", axis=1)
y = data["label"]

# =========================
# Split Data
# =========================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# Train Model
# =========================

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=8,
    random_state=42
)

model.fit(X_train, y_train)

# =========================
# Predictions
# =========================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.4f}")

# =========================
# Classification Report
# =========================

report = classification_report(y_test, y_pred)

print(report)

# Save metrics to file
with open("../model/metrics.txt", "w") as f:
    f.write(f"Accuracy: {accuracy:.4f}\n\n")
    f.write(report)

# =========================
# Confusion Matrix Plot
# =========================

cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(6, 4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")

plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")

plt.savefig("../model/confusion_matrix.png")
plt.close()

# =========================
# Feature Importance Plot
# =========================

importances = model.feature_importances_
features = X.columns

plt.figure(figsize=(8, 5))
sns.barplot(x=importances, y=features)

plt.title("Feature Importance")

plt.savefig("../model/feature_importance.png")
plt.close()

# =========================
# Save Model
# =========================

joblib.dump(model, "../model/brute_force_model.pkl")

print("Model saved successfully!")
print("Metrics and plots saved in model folder.")

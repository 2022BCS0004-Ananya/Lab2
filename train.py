import os
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error, r2_score

# -----------------------------
# Paths
# -----------------------------
DATA_PATH = "dataset/winequality-red.csv"
MODEL_DIR = "output/model"
RESULTS_DIR = "output/results"

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# -----------------------------
# Load dataset
# -----------------------------
data = pd.read_csv(DATA_PATH, sep=';')

X = data.drop("quality", axis=1)
y = data["quality"]

# -----------------------------
# Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Preprocessing (Scaling)
# -----------------------------
'''scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)'''

# -----------------------------
# Model Training
# -----------------------------
model = Lasso(alpha=0.1)
model.fit(X_train, y_train)

# -----------------------------
# Evaluation
# -----------------------------
y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# -----------------------------
# Print metrics (required)
# -----------------------------
print(f"Mean Squared Error (MSE): {mse}")
print(f"R2 Score: {r2}")

# -----------------------------
# Save model
# -----------------------------
model_path = os.path.join(MODEL_DIR, "model.joblib")
joblib.dump(model, model_path)

# -----------------------------
# Save results to JSON
# -----------------------------
results = {
    "mse": mse,
    "r2": r2
}

results_path = os.path.join(RESULTS_DIR, "metrics.json")
with open(results_path, "w") as f:
    json.dump(results, f, indent=4)

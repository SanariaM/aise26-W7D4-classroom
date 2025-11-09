import os, json, joblib
from datetime import datetime
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import pandas as pd

MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def train_and_register():
    df = pd.read_csv("data/user_features.csv")
    X = df[["age", "avg_purchase"]]
    y = [1, 0, 1]

    model = LinearRegression()
    model.fit(X, y)

    y_pred = model.predict(X)
    mse = mean_squared_error(y, y_pred)

    version = datetime.now().strftime("%Y%m%d%H%M%S%f")  # microseconds to avoid collisions
    model_path = f"{MODEL_DIR}/model_{version}.joblib"
    joblib.dump(model, model_path)

    metadata = {"version": version, "mse": float(mse), "timestamp": datetime.now().isoformat()}
    with open(f"{MODEL_DIR}/metadata_{version}.json", "w") as f:
        json.dump(metadata, f, indent=2)

    # -------- Breakout 2 (after you implement experiment_tracking.py) --------
    # from experiment_tracking import log_run
    # log_run(version=version, mse=float(mse), parameters={"model":"LinearRegression","features":"user_features.csv"})

    print(f"Model registered: version={version}, MSE={mse:.3f}")

if __name__ == "__main__":
    train_and_register()

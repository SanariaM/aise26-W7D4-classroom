# experiment_tracking.py
from pathlib import Path
import csv
from datetime import datetime

LOG_PATH = Path("experiment_log.csv")
HEADERS = ["version", "mse", "parameters", "timestamp"]

def log_run(version: str, mse: float, parameters: dict | None = None):
    parameters = parameters or {}
    exists = LOG_PATH.exists()
    with LOG_PATH.open("a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        if not exists:
            w.writeheader()
        w.writerow({
            "version": version,
            "mse": float(mse),
            "parameters": str(parameters),
            "timestamp": datetime.now().isoformat()
        })

def get_best_experiment():
    if not LOG_PATH.exists():
        raise FileNotFoundError("experiment_log.csv not found—train at least once.")
    rows = list(csv.DictReader(LOG_PATH.open()))
    if not rows:
        raise ValueError("experiment_log.csv is empty.")
    def to_f(x):
        try: return float(x)
        except: return float("inf")
    return min(rows, key=lambda r: to_f(r["mse"]))

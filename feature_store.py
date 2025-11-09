import pandas as pd
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def create_feature_table():
    df = pd.DataFrame({
        "user_id": [1, 2, 3],
        "age": [24, 35, 42],
        "avg_purchase": [120.5, 300.0, 89.9],
        "timestamp": [datetime.now()] * 3
    })
    df.to_csv(DATA_DIR / "user_features.csv", index=False)
    print("Feature table created")

def get_features(user_id: int):
    df = pd.read_csv(DATA_DIR / "user_features.csv")
    return df[df["user_id"] == user_id].to_dict(orient="records")[0]


'''# -------- Breakout 1 — TODOs live in the SAME file --------
def add_purchase_frequency_and_save_v2():
    """TODO:
    1) Read DATA_DIR/'user_features.csv'
    2) Add new column 'purchase_frequency' (choose any deterministic rule, e.g. bucket by avg_purchase)
    3) Write to DATA_DIR/'user_features_v2.csv'
    4) Return the output Path
    """
    raise NotImplementedError("Implement Breakout 1 here")

def list_versions():
    """TODO:
    Return a sorted list of filenames in ./data that match 'user_features*.csv'
    Example expected: ['user_features.csv', 'user_features_v2.csv']
    """
    raise NotImplementedError("Implement Breakout 1 here")
'''

if __name__ == "__main__":
    create_feature_table()

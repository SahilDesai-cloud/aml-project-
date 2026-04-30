import os
import joblib
import pandas as pd


def ensure_directories():
    os.makedirs("../results/tables", exist_ok=True)
    os.makedirs("../results/figures", exist_ok=True)
    os.makedirs("../results/models", exist_ok=True)


def save_csv(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)


def save_model(model, path: str):
    joblib.dump(model, path)
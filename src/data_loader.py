import pandas as pd
from pathlib import Path


def load_data():
    path = Path("data/Palo Alto Networks.csv")

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError("The dataset is empty.")

    return df
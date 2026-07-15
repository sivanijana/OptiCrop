from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "dataset" / "Crop_recommendation.csv"

FEATURE_COLUMNS = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]


def load_dataset(path: str | None = None) -> pd.DataFrame:
    data_path = Path(path) if path else DATASET_PATH
    df = pd.read_csv(data_path)
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    for column in FEATURE_COLUMNS + ["label"]:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")
    cleaned = cleaned.dropna()
    cleaned = cleaned.reset_index(drop=True)
    return cleaned


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = clean_dataset(df)
    return cleaned[FEATURE_COLUMNS]

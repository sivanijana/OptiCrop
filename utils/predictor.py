import pickle
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

from utils.preprocessing import FEATURE_COLUMNS


class CropPredictor:
    def __init__(self, model_path: str | Path, label_encoder_path: str | Path):
        self.model_path = Path(model_path)
        self.label_encoder_path = Path(label_encoder_path)
        self.model = None
        self.label_encoder = None
        self.load()

    def load(self):
        if not self.model_path.exists() or not self.label_encoder_path.exists():
            raise FileNotFoundError("Model files not found. Train the model first.")
        with self.model_path.open("rb") as model_file:
            self.model = pickle.load(model_file)
        with self.label_encoder_path.open("rb") as encoder_file:
            self.label_encoder = pickle.load(encoder_file)

    def predict(self, inputs: dict) -> str:
        features = pd.DataFrame([inputs], columns=FEATURE_COLUMNS)
        prediction = self.model.predict(features)[0]
        if isinstance(prediction, str):
            return prediction.strip()
        if hasattr(prediction, "item"):
            prediction = prediction.item()
        try:
            return self.label_encoder.inverse_transform([int(prediction)])[0].strip()
        except Exception:
            return str(prediction).strip()

    def predict_proba(self, inputs: dict) -> np.ndarray:
        features = pd.DataFrame([inputs], columns=FEATURE_COLUMNS)
        probabilities = self.model.predict_proba(features)[0]
        return probabilities

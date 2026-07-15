import pickle
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = BASE_DIR / "dataset" / "Crop_recommendation.csv"
MODEL_DIR = BASE_DIR / "model"


def train_and_save_model():
    df = pd.read_csv(DATASET_PATH)
    df = df.dropna()
    df["label"] = df["label"].astype(str)

    X = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]
    y = df["label"]

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.25, random_state=42, stratify=y_encoded
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=5000),
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
        "KNN": KNeighborsClassifier(n_neighbors=5),
    }

    best_name = None
    best_accuracy = -1
    best_pipeline = None

    for name, model in models.items():
        pipeline = Pipeline([("scaler", StandardScaler()), ("model", model)])
        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, preds)
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_name = name
            best_pipeline = pipeline

    MODEL_DIR.mkdir(exist_ok=True)
    with (MODEL_DIR / "model.pkl").open("wb") as model_file:
        pickle.dump(best_pipeline, model_file)
    with (MODEL_DIR / "label_encoder.pkl").open("wb") as encoder_file:
        pickle.dump(label_encoder, encoder_file)

    return best_name, best_accuracy

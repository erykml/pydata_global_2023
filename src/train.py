import os
from pathlib import Path
import json

import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from constants import DATA_PROCESSED_DIR, MODELS_DIR
from utils import load_params

params = load_params()["train"]

# load training data
X_train = pd.read_csv(f"{DATA_PROCESSED_DIR}/X_train.csv", index_col="Name")
y_train = pd.read_csv(f"{DATA_PROCESSED_DIR}/y_train.csv", index_col="Name")
X_test = pd.read_csv(f"{DATA_PROCESSED_DIR}/X_test.csv", index_col="Name")
y_test = pd.read_csv(f"{DATA_PROCESSED_DIR}/y_test.csv", index_col="Name")

# train a model
model = RandomForestClassifier(random_state=42, **params["params"])
model.fit(X_train, y_train)

# store the trained model
model_dir = Path(MODELS_DIR)
model_dir.mkdir(exist_ok=True)

dump(model, f"{MODELS_DIR}/model.joblib")

# obtain predictions + evaluate
y_pred = model.predict(X_test)

metrics = {
    "accuracy": round(accuracy_score(y_test, y_pred), 4),
    "recall": round(recall_score(y_test, y_pred), 4),
    "precision": round(precision_score(y_test, y_pred), 4),
    "f1_score": round(f1_score(y_test, y_pred), 4),
}

json.dump(obj=metrics, fp=open("metrics.json", "w"), indent=4, sort_keys=True)

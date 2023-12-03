import json
import os
from pathlib import Path

import pandas as pd
from dvclive.lgbm import DVCLiveCallback
from joblib import dump
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

from constants import DATA_PROCESSED_DIR, MODELS_DIR
from dvclive import Live
from utils import load_params

params = load_params()["train"]

# load training data
X_train = pd.read_csv(f"{DATA_PROCESSED_DIR}/X_train.csv", index_col="Name")
y_train = pd.read_csv(f"{DATA_PROCESSED_DIR}/y_train.csv", index_col="Name")

# train a model
model = LGBMClassifier(random_state=42, objective="binary", **params["params"])

with Live(save_dvc_exp=True) as live:
    print("Training the model ----")

    # for simplicity, we use the training set as validation set
    fit_params = {
        "eval_set": [(X_train, y_train)],
        "eval_names": ["valid"],
        "callbacks": [DVCLiveCallback(live=live)],
    }
    model.fit(X_train, y_train, **fit_params)
    print("Training completed. Storing the model...")

    # store the trained model
    model_dir = Path(MODELS_DIR)
    model_dir.mkdir(exist_ok=True)

    dump(model, f"{MODELS_DIR}/model.joblib")

    print("Done!")

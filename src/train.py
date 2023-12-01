import os
from pathlib import Path
import json

import pandas as pd
from joblib import dump
from sklearn.metrics import accuracy_score, precision_score, recall_score
from lightgbm import LGBMClassifier

from constants import DATA_PROCESSED_DIR, MODELS_DIR
from utils import load_params

from dvclive import Live
from dvclive.lgbm import DVCLiveCallback

params = load_params()["train"]

# load training data
X_train = pd.read_csv(f"{DATA_PROCESSED_DIR}/X_train.csv", index_col="Name")
y_train = pd.read_csv(f"{DATA_PROCESSED_DIR}/y_train.csv", index_col="Name")
X_test = pd.read_csv(f"{DATA_PROCESSED_DIR}/X_test.csv", index_col="Name")
y_test = pd.read_csv(f"{DATA_PROCESSED_DIR}/y_test.csv", index_col="Name")

# train a model
# model = RandomForestClassifier(random_state=42, **params["params"])
model = LGBMClassifier(random_state=42, objective="binary", **params["params"])

with Live(save_dvc_exp=True) as live:
    # for simplicity, we use the training set as validation set
    fit_params = {
        "eval_set": [(X_test, y_test)],
        "eval_names": ["valid"],
        "callbacks": [DVCLiveCallback(live=live)],
    }
    model.fit(X_train, y_train, **fit_params)

    # store the trained model
    model_dir = Path(MODELS_DIR)
    model_dir.mkdir(exist_ok=True)

    dump(model, f"{MODELS_DIR}/model.joblib")

    # obtain predictions
    y_pred = model.predict(X_test)
    y_pred_prob = model.predict_proba(X_test)[:, 1]
    y_test_array = y_test.values.ravel()

    # evaluate - get metrics + plots
    live.log_sklearn_plot("confusion_matrix", y_test_array, y_pred)
    live.log_sklearn_plot("roc", y_test_array, y_pred_prob)
    live.log_sklearn_plot("precision_recall", y_test_array, y_pred_prob)

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
    }

    json.dump(obj=metrics, fp=open("metrics.json", "w"), indent=4, sort_keys=True)

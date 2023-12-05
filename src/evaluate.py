import json

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score

from constants import DATA_PROCESSED_DIR, MODELS_DIR
from dvclive import Live

# Load the model
model = joblib.load(f"{MODELS_DIR}/model.joblib")

# load test data
X_test = pd.read_csv(f"{DATA_PROCESSED_DIR}/X_test.csv", index_col="Name")
y_test = pd.read_csv(
    f"{DATA_PROCESSED_DIR}/y_test.csv", index_col="Name"
).values.ravel()

# obtain predictions
y_pred = model.predict(X_test)
y_pred_prob = model.predict_proba(X_test)[:, 1]

# evaluate - get metrics + plots
with Live("results/evaluate") as live:
    live.log_sklearn_plot("confusion_matrix", y_test, y_pred)
    live.log_sklearn_plot("roc", y_test, y_pred_prob)
    live.log_sklearn_plot("precision_recall", y_test, y_pred_prob)

    metrics = {
        "accuracy": round(accuracy_score(y_test, y_pred), 4),
        "recall": round(recall_score(y_test, y_pred), 4),
        "precision": round(precision_score(y_test, y_pred), 4),
    }
    print(metrics)

    json.dump(obj=metrics, fp=open("metrics.json", "w"), indent=4, sort_keys=True)

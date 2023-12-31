import warnings
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from dvc.api import params_show
from dvclive import Live
from dvclive.lgbm import DVCLiveCallback
from joblib import dump
from lightgbm import LGBMClassifier, plot_importance

from constants import CUSTOM_PLOTS_DIR, DATA_PROCESSED_DIR, MODELS_DIR

warnings.filterwarnings("ignore", category=UserWarning, module="lightgbm")

params = params_show()["train"]

# load training data
X_train = pd.read_csv(f"{DATA_PROCESSED_DIR}/X_train.csv", index_col="Name")
y_train = pd.read_csv(
    f"{DATA_PROCESSED_DIR}/y_train.csv", index_col="Name"
).values.ravel()

# train a model
model = LGBMClassifier(random_state=42, objective="binary", **params["params"])

with Live("results/train") as live:
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

    ax = plot_importance(model, importance_type="split")
    feat_imp_plot_path = f"{CUSTOM_PLOTS_DIR}/feat_importance.png"
    plt.savefig(feat_imp_plot_path)
    live.log_image("feat_importance.png", feat_imp_plot_path)

    print("Done!")

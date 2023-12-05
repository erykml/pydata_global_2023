import os
from pathlib import Path

import pandas as pd
from dvc.api import params_show
from sklearn.model_selection import train_test_split

from constants import DATA_PROCESSED_DIR, DATA_RAW_DIR

# settings
FEATURE_LIST = [
    "Total",
    "HP",
    "Attack",
    "Defense",
    "Sp. Atk",
    "Sp. Def",
    "Speed",
    # "Generation",
]
TARGET = "Legendary"

# get the params
params = params_show()["prepare_data"]

# load data
df = pd.read_csv(os.path.join(DATA_RAW_DIR, "pokedex.csv")).set_index("Name")

# additional pre-processing
if not params["include_mega_evol"]:
    df = df.loc[~df["Mega Evolution"]]

df = df.query(f"Generation <= {params['max_generation']}")

# keeping only the requested features
y = df.pop(TARGET)
X = df[FEATURE_LIST]

# train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=params["test_size"], random_state=42, stratify=y
)

# saving data
data_processed_path = Path(DATA_PROCESSED_DIR)
data_processed_path.mkdir(exist_ok=True)

X_train.to_csv(f"{DATA_PROCESSED_DIR}/X_train.csv")
X_test.to_csv(f"{DATA_PROCESSED_DIR}/X_test.csv")
y_train.to_csv(f"{DATA_PROCESSED_DIR}/y_train.csv")
y_test.to_csv(f"{DATA_PROCESSED_DIR}/y_test.csv")

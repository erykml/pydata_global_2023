import itertools
import subprocess
import itertools

# param values
n_estimators_grid = [10, 100]
max_depth_grid = [5, "null"]
class_weight_grid = ["balanced", "null"]

for n_est, max_depth, class_weight in itertools.product(
    n_estimators_grid, max_depth_grid, class_weight_grid
):
    subprocess.run(
        [
            "dvc",
            "exp",
            "run",
            "--queue",
            "--set-param",
            f"train.params.n_estimators={n_est}",
            "--set-param",
            f"train.params.max_depth={max_depth}",
            "--set-param",
            f"train.params.class_weight={class_weight}",
        ]
    )

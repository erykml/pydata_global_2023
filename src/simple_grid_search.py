import itertools
import subprocess
import itertools

# param values
n_estimators_grid = [10, 20]
max_depth_grid = [5, 10]

for n_est, max_depth in itertools.product(n_estimators_grid, max_depth_grid):
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
        ]
    )

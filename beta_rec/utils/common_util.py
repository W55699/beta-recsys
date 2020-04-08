import os
import random
import time
import numpy as np
import torch
import pandas as pd

UTILS_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(UTILS_ROOT, "..", ".."))

configs = BASE_DIR + "/configs/"
datasets = BASE_DIR + "/datasets/"
checkpoints = BASE_DIR + "/checkpoints/"
results = BASE_DIR + "/results/"
logs = BASE_DIR + "/logs/"
samples = BASE_DIR + "/samples/"
runs = BASE_DIR + "/runs/"

for DIR in [configs, datasets, checkpoints, results, samples, logs, runs]:
    if not os.path.exists(DIR):
        os.makedirs(DIR)


def timeit(method):
    """
    Decorator for tracking the execution time for the specific method
    Args:
        method: The method need to timeit.

    To use:
        @timeit
        def method(self):
            pass
    
    """

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            print(
                "Execute [{}] method costing {:2.2f} ms".format(
                    method.__name__, (te - ts) * 1000
                )
            )
        return result

    return timed


def save_to_csv(result, result_file):
    """
    Save a result dict to disk.

    Args:
        result: The result dict to be saved.
        result_file: The file path to be saved.

    Returns:
        None

    """
    result_df = pd.DataFrame(result)
    if os.path.exists(result_file):
        print(result_file, " already exists, appending result to it")
        total_result = pd.read_csv(result_file)
        total_result = total_result.append(result_df)
    else:
        print("Create new result_file:", result_file)
        total_result = result_df
    total_result.to_csv(result_file, index=False)


def set_seed(seed):
    """
    Initialize all the seed in the system

    Args:
        seed: A global random seed.

    """
    if type(seed) != int:
        raise ValueError("Error: seed is invalid type")
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
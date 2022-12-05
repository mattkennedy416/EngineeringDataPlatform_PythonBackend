
"""
Types of interfaces to get data from its original format into this python instance's memory
- load csv from disk
- load table from database
"""

import numpy as np
import pandas as pd

def extract_example(config):
    # "extract" functions have no inputs and multiple outputs
    return np.random.randint(0, 10, (25,))


def read_csv(config):
    path = config.get('path', None)
    data = pd.read_csv(path)
    return data


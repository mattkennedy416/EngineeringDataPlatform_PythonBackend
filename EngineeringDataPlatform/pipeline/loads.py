
"""
Types of interfaces to push data to external systems such as:
- push to databases on other servers
- making API calls
- publish to Kafka streams
- writing data to disk in some other format (pickle, csv, excel, etc)
"""

import numpy as np

def load_example(config, prev_step_output):
    # "load" functions have multiple inputs and no outputs
    # each load function should specify what they're expecting the args and kwargs to be
    print(prev_step_output)



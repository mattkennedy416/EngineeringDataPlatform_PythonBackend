
"""
As an interim solution this file in its entirety is getting directly injected into IPython environments
"""


import numpy as np
import pandas as pd


def etl_load_csv(filename):

    #filename = request_content.get('filename')

    data = pd.read_csv(filename)
    return data





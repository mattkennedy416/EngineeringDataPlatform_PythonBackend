

import warnings

import numpy as np
import pandas as pd

from EngineeringDataPlatform.table.Table import Table

from sklearn import preprocessing

"""
@tag=
@config_params=[]
@valid_input=[]
@valid_output=[]
@description=""
@working_example=""
"""


def StandardScalar(config, prev_step_output):
    """
    @tag=cleaning.normalization
    @config_params=[]
    @valid_input=[np.array, pd.DataFrame, edp.Table]
    @valid_output=[dict({'scalar': sklearn.StandardScalar, 'scaled_values': np.array})]
    @description=Allow a reference to a python function to be passed in through a config
    @working_example=""
    """

    if isinstance(prev_step_output, (pd.DataFrame, Table)):
        values = prev_step_output.values
    else:
        values = prev_step_output

    scalar = preprocessing.StandardScaler()
    scaled_values = scalar.fit_transform(values)

    return {'scalar': scalar, 'scaled_values': scaled_values}


def drop_na_rows(config, prev_step_output):
    """
    @tag=cleaning.bad_values
    @config_params=[(how, default='any', str, {'any','all'}), (columns_to_consider, default=None, list(col_names), columns_to_consider=['a','b','c'] will only look in columns 'a', 'b', and 'c' for missing values)]
    @valid_input=[pd.DataFrame, edp.Table]
    @valid_output=[]
    @description="Remove rows that have missing values. Specifying 'any'/'all' as well as the optional list of columns to consider enable the removal of rows based on almost any condition."
    @working_example=""
    """
    #inplace = config.get('inplace', False)
    how = config.get('how', 'any')
    columns_to_consider = config.get('columns_to_consider', None)

    return prev_step_output.dropna(axis=0, how=how, subset=columns_to_consider)



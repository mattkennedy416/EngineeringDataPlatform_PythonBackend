
"""
Manipulating, splitting, joining, and more; enable arbitary python and SQL code execution
focus here should be enabling the access of data and ensuring dependencies and inputs have been updated

SQL queries require that all inputs have been written back to workspace database, python transforms can stay in memory
or be writen back
"""
import warnings

import numpy as np
import pandas as pd
from EngineeringDataPlatform.table.Table import Table

def transform_example(config, prev_step_output):
    # "transform" functions have multiple inputs and multiple outputs?
    # each transform should specify what they're expecting the args and kwargs to be
    return prev_step_output * config.get('multiplyBy', 2)


def python_funcRef_from_config(config, prev_step_output):
    """
    @tag=custom_code.python
    @config_params=[('func', 'required', 'python function ref', def myCustomFunction(config, prev_step_output):\n    return prev_step_output['a']*2\nmyCustomFunction)]
    @valid_input=[any]
    @valid_output=[any]
    @description=Allow a reference to a python function to be passed in through a config
    @working_example=""
    """
    func = config.get('funcRef', None)
    return func(config, prev_step_output)


def python_funcStr_from_config(config, prev_step_output):
    """
    @tag=custom_code.python
    @config_params=[(funcStr), (funcName)]
    @valid_input=[any]
    @valid_output=[any]
    @description=Allow a string of a python function to be passed in through a config
    @working_example=""
    """
    funcStr = config.get('funcStr', None)
    funcName = config.get('funcName', None)
    eval(funcStr)
    return locals()[funcName](config, prev_step_output)


def column_names_replace(config, prev_step_output):
    """
    @tag=tables.columns
    @config_params=[(values), (inplace)]
    @valid_input=[any]
    @valid_output=[any]
    @description=Replace the column names in a Table or pd.DataFrame with a list of new values
    @working_example=""
    """
    newVals = config.get('values', [])
    inPlace = config.get('inplace', False)

    assert len(newVals) == prev_step_output.shape[1]

    map = {}
    for n, col in enumerate(prev_step_output.columns.values):
        map[col] = newVals[n]

    if inPlace:
        prev_step_output.rename(mapper=map, axis=1, inplace=True)
        return prev_step_output
    else:
        new_output = prev_step_output.rename(mapper=map, axis=1, inplace=False)
        return new_output


def column_names_strmodify(config, prev_step_output):
    """
    @tag=tables.columns
    @config_params=[(values), (inplace)]
    @valid_input=[any]
    @valid_output=[any]
    @description=Modify the column names by passing in string manipulation code that will be individually applied to each column
    @working_example=".replace('<', '').replace('>', '').strip()"
    """
    raise NotImplementedError()


def column_names_funcmodify(config, prev_step_output):
    """
    @tag=tables.columns
    @config_params=[(func), (inplace)]
    @valid_input=[any]
    @valid_output=[any]
    @description=Modify the column names by passing in a function that will be individually applied to each item
    @working_example=""
    """

    func = config.get('func', None)
    inPlace = config.get('inplace', False)

    map = {}
    for n, col in enumerate(prev_step_output.columns.values):
        map[col] = func(col)

    if inPlace:
        prev_step_output.rename(mapper=map, axis=1, inplace=True)
        return prev_step_output
    else:
        new_output = prev_step_output.rename(mapper=map, axis=1, inplace=False)
        return new_output


def split_by_categorical_col_value(config, prev_step_output):
    """
    @tag=tables.filter
    @config_params=[(col)]
    @valid_input=[any]
    @valid_output=[any]
    @description=Split a large dataframe or table into a list of many dataframes based on a single column of categorical values eg - stock market data with 20 tickers combined into a single source, lets split them into 20 sources
    @working_example=""
    """
    col = config.get('col', None)
    col_vals = prev_step_output[col].values

    unique = np.unique(col_vals)
    outputs = []
    for val in unique:
        ind = col_vals == val
        subsetTable = prev_step_output.iloc[ind, :]
        subsetTable.reset_index(inplace=True)
        outputs.append(subsetTable)

    return outputs


def filter_list_by_func(config, prev_step_output):
    """
    @tag=tables.filter
    @config_params=[(func)]
    @valid_input=[any]
    @valid_output=[any]
    @description=Filter a list of objects by some function that takes the object as an input and returns a True or False
    @working_example=""
    """
    func = config.get('func', None)
    return [obj for obj in prev_step_output if func(obj)]

def take_sample_from_list(config, prev_step_output):
    """
    @tag=tables.sampling
    @config_params=[(sample_method), (sample_num), (random_seed)]
    @valid_input=[any]
    @valid_output=[any]
    @description=Down-select a large list of objects to a small list of objects for inspection or testing
    @working_example=""
    """
    default_sample_num = 10
    sample_method = config.get('sample_method', None) # {random, first, last}
    sample_num = config.get('sample_num', default_sample_num) # positive integer, will automatically clamp this so we don't error out if the list is smaller than expecting
    random_seed = config.get('random_seed', None) # optionally provide a np.random.seed() value to generate a consistently random selection

    if sample_num <= 0: # in case this is being generated programatically somehow
        warnings.warn('take_sample_from_list -> sample_num is less than 0')
        sample_num = default_sample_num
    if sample_num > len(prev_step_output): # could also have a small list mixed in with bigger lists
        sample_num = prev_step_output

    if sample_method == 'random':
        if random_seed is not None:
            np.random.seed(random_seed)

        selection = np.random.randint(0, len(prev_step_output), (sample_num,))
        return [prev_step_output[n] for n in selection]

    elif sample_method == 'first':
        return prev_step_output[:sample_num]

    elif sample_method == 'last':
        return prev_step_output[-sample_num:]

    else:
        raise ValueError('Unknown or no sample_method specified')



def commit_to_workspace_db(config, prev_step_output):
    """

    @tag=workspace.commit
    @config_params=[(if_exists, default='replace', str, {'fail','replace','append'}), (table_name_method, required, str, {'func', 'str', 'dict', 'preinitialized'})]
    @valid_input=[any]
    @valid_output=[any]
    @description=Commit the input to the workspace database.
    @working_example=""
    """
    if_exists = config.get('if_exists', 'replace')
    table_name_method = config.get('table_name_method', None) # {func, str, dict, preinitialized} <- these are our 4 cases, must specify one
    assert table_name_method is not None

    workspace = config.get('_workspace')

    # if both of these are none, we can also pass in a Table pre-initialized by something else and we'll just commit
    # we could also do a dictionary where the keys are the tablename..

    if not isinstance(prev_step_output, (list, tuple, dict)):
        prev_step_output = list(prev_step_output) # <- is this going to mess with the obj references in the calling functions? it might, python is weird

    output_tables = []
    for item in prev_step_output: # assume we're some kind of collection now

        if table_name_method == 'func':
            table_name = config.get('func', None)(item)
            table = Table(item)
            table.initialize(workspace, table_name)
        elif table_name_method == 'str':
            table_name = config.get('name', None)
            table = Table(item)
            table.initialize(workspace, table_name)
        elif table_name_method == 'dict':
            table_name = item
            table = Table(prev_step_output[item])
            table.initialize(workspace, table_name)
        elif table_name_method == 'preinitialized':
            table = item
        else:
            raise ValueError('Unknown or no table_name_method specified')

        success = table.commit(if_exists=if_exists)
        if success:
            output_tables.append(table)
        else:
            output_tables.append(None)

    return output_tables








def run_subsequent_pipeline_per_item(config, prev_step_output):
    """
    @tag=tables.columns
    @config_params=[]
    @valid_input=[any]
    @valid_output=[any]
    @description=When we split one table/dataframe into many tables/dataframes, we may want to run subsequent transforms and loads PER TABLE rather than defining new transforms and loads that appropriately can process multiple tables
    @working_example=""
    """

    # probably need to get the pipeline.execute() to search for this and run a for loop?
    pass
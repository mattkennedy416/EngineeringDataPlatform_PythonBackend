
"""
Return a variable loaded in the local environment to a format that can be displayed as
as a table in a frontend notebook.
"""

import numpy as np
import pandas as pd
import json


def inspect_tableView(varDict, variable, maxRows=50, precision=6):


    if variable not in varDict:
        raise KeyError('Variable ' + str(variable) + ' could not be found in environment.')

    # otherwise what are our core types going to be here?

    obj = varDict[variable]


    if isinstance(obj, np.ndarray):
        headers = ['Col ' + str(n) for n in range(obj.shape[1])]

        numRows = np.min((maxRows, obj.shape[0]))
        rows = list(obj[0:numRows])

    elif isinstance(obj, pd.DataFrame):
        headers = obj.columns.values
        numRows = np.min((maxRows, obj.shape[0]))

        rows = list(obj.values[0:numRows, :])

    else:
        raise TypeError('Unknown object type ' + str(type(variable)) + ' cast as np.ndarray, pd.DataFrame, or edp.Table')


    # lets assume we convert these to a more universal format where we can build one JSON formatter

    rowData = []
    for m, row in enumerate(rows):
        rowSingleDict = {"id": str(m)}
        for n, col in enumerate(headers):
            rowSingleDict[col.lower()] = str(np.round(row[n], precision)) # convert to string so we don't lose our precision
        rowData.append(rowSingleDict)

    headerData = []
    for col in headers:
        headerData.append({'key': col.lower(), 'value': col})

    # raise TypeError(json.dumps({'headers': headerData,
    #                     'rows': rowData}))

    return json.dumps({'headers': headerData,
                        'rows': rowData})



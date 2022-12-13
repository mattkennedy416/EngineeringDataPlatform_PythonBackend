
"""
Return a variable loaded in the local environment to a format that can be displayed as
as a table in a frontend notebook.
"""

import numpy as np
import pandas as pd


def inspect_tableView(varDict, variable, maxRows=50, precision=6):

    if variable not in varDict:
        raise KeyError('Variable ' + str(variable) + ' could not be found in environment.')

    # otherwise what are our core types going to be here?

    obj = varDict[variable]


    if isinstance(obj, np.ndarray):
        headers = ['Col ' + str(n) for n in range(obj.shape[1])]

        numRows = np.min((maxRows, obj.shape[0]))
        rows = list(obj[0:numRows])

    else:
        raise TypeError('Unknown object type ' + str(type(variable)) + ' cast as np.ndarray, pd.DataFrame, or edp.Table')


    # lets assume we convert these to a more universal format where we can build one JSON formatter

    rowData = []
    for row in rows:
        rowSingleDict = {}
        for n, col in enumerate(headers):
            rowSingleDict[col] = str(np.round(row[n], precision)) # convert to string so we don't lose our precision
        rowData.append(rowSingleDict)

    headerData = []
    for col in headers:
        headerData.append({'key': col.lower(), 'value': col})


    return {'headers': headerData,
            'rows': rowData}



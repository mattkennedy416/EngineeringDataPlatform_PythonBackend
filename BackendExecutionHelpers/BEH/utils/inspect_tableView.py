
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
        rows = obj[0:numRows].tolist()

    elif isinstance(obj, pd.DataFrame):
        headers = obj.columns.values.tolist()
        numRows = np.min((maxRows, obj.shape[0]))

        rows = obj.values[0:numRows, :].tolist()

    else:
        raise TypeError('Unknown object type ' + str(type(variable)) + ' cast as np.ndarray, pd.DataFrame, or edp.Table')


    # format for antd table is:
    # [{"id": 0, "col0": "c0", "col1": "c1"}, {"id": 1, "col0": "row1", "col1": "row1"}]
    outputRows = []
    for rowNum, row in enumerate(rows):
        reformatted = {"id": rowNum}
        for colNum, header in enumerate(headers):
            reformatted[header] = row[colNum]
        outputRows.append(reformatted)

    return json.dumps({'variable': variable,
                        'data': outputRows,
                       'headers': headers})





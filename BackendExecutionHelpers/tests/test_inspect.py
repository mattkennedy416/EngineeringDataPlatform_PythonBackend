
from BackendExecutionHelpers.BEH.utils.inspect_tableView import inspect_tableView

import numpy as np
import pandas as pd
import json


def test_inspect_tableView_npArray():
    a = np.random.rand(5,5)
    vars = locals()

    output = inspect_tableView(vars, variable='a', maxRows=25, precision=5)
    assert output is not None

    parsed = json.loads(output)
    assert 'data' in parsed
    assert len(parsed['data']) == 5


def test_inspect_tableView_pdDataFrame():
    a = np.random.rand(5,5)
    df = pd.DataFrame(data=a, columns=['a','b','c','d','e'])
    vars = locals()

    output = inspect_tableView(vars, variable='df', maxRows=25, precision=5)
    assert output is not None

    parsed = json.loads(output)
    assert 'data' in parsed
    assert len(parsed['data']) == 5


if __name__ == '__main__':
    test_inspect_tableView_pdDataFrame()
    test_inspect_tableView_npArray()

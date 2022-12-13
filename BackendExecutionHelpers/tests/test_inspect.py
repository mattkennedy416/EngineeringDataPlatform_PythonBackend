
from BackendExecutionHelpers.BEH.utils.inspect_tableView import inspect_tableView

import numpy as np


def test_inspect_tableView():
    a = np.random.rand(5,5)
    vars = locals()

    output = inspect_tableView(vars, 'a')
    assert output is not None


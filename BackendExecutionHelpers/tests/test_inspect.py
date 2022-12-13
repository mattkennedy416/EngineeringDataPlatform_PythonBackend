
from BackendExecutionHelpers.BEH.utils.inspect_tableView import inspect_tableView

import numpy as np


def test_inspect_tableView():
    a = np.random.rand(5,5)
    vars = locals()

    output = inspect_tableView(vars, variable='a', maxRows=25, precision=5)
    assert output is not None


if __name__ == '__main__':
    test_inspect_tableView()

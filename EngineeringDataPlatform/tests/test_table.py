
import EngineeringDataPlatform as edp
import numpy as np
import pandas as pd


def test_tableCreation():
    workspace = edp.workspace.create_workspace_if_not_existing("workspace_test")
    table = edp.Table(columns=['a', 'b', 'c'], data=np.random.rand(150, 3))
    table.initialize(workspace, 'random_table')

    assert table.name() == 'random_table'
    assert table.workspace().name() == workspace.name()
    assert table.shape == (150, 3)


def test_selectWhere():
    workspace = edp.workspace.create_workspace_if_not_existing("workspace_test")
    table = edp.Table(columns=['a', 'b', 'c'], data=np.random.rand(150, 3))
    table.initialize(workspace, 'random_table')
    table.commit()

    results = table.select_where('a<0.5', return_cols=['b', 'c'])

    assert results.workspace().name() == workspace.name()
    assert results.shape[0] < 150
    assert results.shape[1] == 2

def test_equalsApprox():
    workspace = edp.workspace.create_workspace_if_not_existing("workspace_test")
    table = edp.Table(columns=['a', 'b', 'c'], data=np.random.rand(150, 3))
    table.initialize(workspace, 'random_table')

    table2 = edp.Table(columns=['a', 'b', 'c'], data=np.random.rand(150, 3))
    table2.initialize(workspace, 'random_table2')

    assert table.equals_approx(table2)



test_equalsApprox()
test_tableCreation()
test_selectWhere()




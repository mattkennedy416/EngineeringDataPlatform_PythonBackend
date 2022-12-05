

import EngineeringDataPlatform as dep
import numpy as np
import pandas as pd


def test_createWorkspace():
    workspace_name = "workspace1"
    workspace = dep.workspace.create_workspace_if_not_existing(workspace_name)

    assert workspace is not None


def test_findWorkspace():
    workspace_name = "workspace1"
    workspace = dep.workspace.create_workspace_if_not_existing(workspace_name)

    w = dep.workspace.findWorkspaceInEnv(locals(), globals())
    
    assert w is not None
    assert w.name() == workspace.name()


def test_sql():
    workspace = dep.workspace.create_workspace_if_not_existing("workspace_test")
    table = dep.Table(columns=['a', 'b', 'c'], data=np.random.rand(150, 3))
    table.initialize(workspace, 'random_table')
    table.commit()

    results_workspace = workspace.sql('SELECT * FROM random_table WHERE a < 0.5')
    results_table = table.sql('SELECT * FROM random_table WHERE a < 0.5')

    assert results_table.workspace() == results_workspace.workspace()
    assert results_workspace.shape == results_table.shape


def test_loadTableFromDatabase():
    workspace = dep.workspace.create_workspace_if_not_existing("workspace_test")
    table = dep.Table(columns=['a', 'b', 'c'], data=np.random.rand(150, 3))
    table.initialize(workspace, 'random_table')
    table.commit()

    table_loaded = workspace.load_table_from_database('random_table')
    assert table_loaded.shape == (150,3)



test_findWorkspace()
test_loadTableFromDatabase()
test_sql()
test_createWorkspace()


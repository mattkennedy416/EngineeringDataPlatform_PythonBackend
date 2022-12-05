
import EngineeringDataPlatform as dep

import numpy as np
import pandas as pd



workspace_name = "workspace1"

workspace = dep.workspace.create_workspace_if_not_existing(workspace_name)

#w = dep.workspace.findWorkspaceInEnv(globals())




print()
table = dep.Table(columns=['a','b','c'], data=np.random.rand(15000,3))
table.initialize(workspace, 'random_table')


pd.DataFrame(columns=['a','b','c'], data=np.random.rand(10,3))

table.commit()
table.sql('SELECT * from random_table')














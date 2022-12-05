
import EngineeringDataPlatform as dep
from EngineeringDataPlatform.workspace.CreateNewWorkspace import _createNewPostgresDatabase, _checkIfPostgresDatabaseExists, create_workspace_if_not_existing, _deleteWorkspace
from EngineeringDataPlatform.workspace.WorkspaceHelpers import findWorkspaceInEnv, alreadyInWorkspace, exists, find




def test_createAndDeleteWorkspace():
    workspace = dep.workspace.create_workspace_if_not_existing("test2")
    dbCreated = _checkIfPostgresDatabaseExists(workspace.name())

    assert dbCreated

    _deleteWorkspace(workspace.name())
    dbExistsAfterDelete = _checkIfPostgresDatabaseExists(workspace.name())

    assert not dbExistsAfterDelete



test_createAndDeleteWorkspace()




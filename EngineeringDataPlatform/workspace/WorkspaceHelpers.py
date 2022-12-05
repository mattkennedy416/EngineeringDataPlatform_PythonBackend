
from EngineeringDataPlatform.workspace.Workspace import Workspace


def exists(name):
    # how do we check if a workspace exists?
    pass


def find():
    # how do we find all of the already existing workspaces?
    pass


def alreadyInWorkspace(locals, globals):
    # within individual processes at this level, we should only ever be writing code and doing analysis within a single workspace
    # can we safely query the globals to get our workspace?
    if findWorkspaceInEnv(locals, globals) is None:
        return False
    else:
        return True


def findWorkspaceInEnv(locals, globals):
    for name in globals:
        if isinstance(globals[name], Workspace):
            return globals[name]
    for name in locals:
        if isinstance(locals[name], Workspace):
            return locals[name]
    return None






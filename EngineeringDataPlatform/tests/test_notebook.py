

from EngineeringDataPlatform.workspace.Notebook import Notebook
from EngineeringDataPlatform import workspace

def test_loadNotebook():
    localProjectSpace = "~/Documents/EngineeringDataPlatform/ProjectSpace/"
    project = workspace.Project(localProjectSpace, 'testProject')

    notebook = project.ReadNotebook('testNotebook.edpnb')

    assert notebook.name() == 'testNotebook'

    content = notebook.toDict()

    assert len(content['cellContents']) > 0

def test_addNewCell():
    localProjectSpace = "~/Documents/EngineeringDataPlatform/ProjectSpace/"
    project = workspace.Project(localProjectSpace, 'testProject')

    notebook = project.ReadNotebook('testNotebook.edpnb')

    confirm = notebook.createNewCellAtEnd(cellType='code', cellSyntax='python')

    content = notebook.getCell_byID(confirm['cellID'])
    assert content is not None

    content2 = notebook.getCell_byIndex(confirm['cellIndex'])
    assert content2 is not None
    assert content['cellID'] == content2['cellID']




if __name__ == '__main__':
    test_loadNotebook()
    test_addNewCell()


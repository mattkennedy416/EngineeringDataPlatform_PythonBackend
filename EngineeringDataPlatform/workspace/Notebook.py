

import datetime
import uuid
from flask import jsonify
class Notebook:


    def __init__(self, workspace, notebookContents=None):

        if notebookContents is None:
            self.cellContents = []
            self.notebookName = self.generateNotebookName()
        else:
            self.cellContents = notebookContents['cellContents']
            self.notebookName = notebookContents['notebookName']

        self.workspace = workspace

    def name(self):
        return self.notebookName
    def toDict(self):
        """
        this should be the truth for our notebook schema
        """
        return {'notebookFilename': self.notebookName,
                'cellContents': self.cellContents}

    def toJSON(self):
        return jsonify(self.toDict())

    def generateNotebookName(self):
        return 'myNotebookName'

    def generateCellID(self):
        return '.'.join([self.workspace.name(),
                self.notebookName,
                str(uuid.uuid4())])

    def setContent(self, cellContents):
        self.cellContents = cellContents


    def createNewCellAtEnd(self, cellType='code', cellSyntax='python'):
        newContents = {
            "cellContent": "",
            "cellID": self.generateCellID(),
            "cellSyntax": cellSyntax,
            "cellType": cellType
        }
        self.cellContents.append(newContents)

        return {'cellIndex': len(self.cellContents)-1,
                'cellID': self.cellContents[-1]['cellID']}

    def getCell_byIndex(self, index):
        """
        request the content of a specific cell by its index
        """
        if len(self.cellContents) >= index:
            return self.cellContents[index]
        else:
            print('requested the cell at index', index, 'while there are only', len(self.cellContents), 'cells in the noteobok')
            return None


    def getCell_byID(self, ID):
        """
        request the content of a specific cell by its index
        """
        # we could index this but probably not worth it?
        # depends if we're going to let them reorganize the order of things
        for cell in self.cellContents:
            if cell['cellID'] == ID:
                return cell

        print('could not find a cell with cellID', ID, 'in notebook', self.name())
        return None

















import datetime
import uuid
import json
from flask import jsonify
class Notebook:


    def __init__(self, project, notebookContents=None, pathInProject=None):

        self.pathInProject = pathInProject

        if notebookContents is None:
            self.cellContents = []
            self.notebookName = self.generateNotebookName()
        else:
            self.cellContents = notebookContents['cellContents']
            self.notebookName = notebookContents['notebookName']

        self.project = project

    def name(self):
        return self.notebookName

    def save(self):
        """
        basic save operation, assume we're aleady configured and just updating content
        """
        if self.pathInProject is None:
            return {'error': 'notebook does not have a save path defined'}

        absPath = self.project.pathInProjecttoAbsolutePath(self.pathInProject)
        with open(absPath, 'w') as f:
            json.dump(self.toDict(), f, indent=2)

    def toDict(self):
        """
        this should be the truth for our notebook schema
        """
        return {'notebookPath': self.pathInProject,
                'notebookName': self.name(),
                'cellContents': self.cellContents}

    def toJSON(self):
        return jsonify(self.toDict())

    def generateNotebookName(self):
        return 'myNotebookName'

    def generateCellID(self):
        return '.'.join([self.project.name(),
                self.notebookName,
                str(uuid.uuid4())])

    def setContent(self, cellContents):
        self.cellContents = cellContents

    def updateContent(self, cellContents):
        """
        iterate through and update the cells of matching cellIDs
        cells that are not changing don't need to be passed
        """
        if isinstance(cellContents, dict): # if only a single cell was passed
            cellContents = [cellContents]

        for updatedCell in cellContents:
            for n, existingCell in enumerate(self.cellContents):
                if existingCell['cellID'] == updatedCell['cellID']:
                    self.cellContents[n] = updatedCell
                    break



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















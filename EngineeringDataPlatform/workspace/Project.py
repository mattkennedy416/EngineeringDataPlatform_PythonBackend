
"""
Do whatever folder creation and environment setup we need to do on the local disk
so that we can start getting persistent files.
"""

import os
import json
from flask import jsonify
from EngineeringDataPlatform.workspace.Notebook import Notebook


class Project:

    def __init__(self, localProjectSpaceDir, projectName):

        self.projectName = projectName

        if localProjectSpaceDir[0] == '~':
            localProjectSpaceDir = localProjectSpaceDir.replace('~', os.path.expanduser('~').replace('\\', '/'))

        self.projectDir = os.path.join(localProjectSpaceDir, projectName)

        self.notebookDir = os.path.join(self.projectDir, 'notebooks')
        self.pipelinesDir = os.path.join(self.projectDir, 'pipelines')

        if not os.path.isdir(self.projectDir):
            # need to create whatever folder structure we need
            self._createEmptyProject()

        self.loadedNotebooks = {}

    def name(self):
        return self.projectName
    def _createEmptyProject(self):

        os.makedirs(self.projectDir)

        # what else do we need in here?
        # probably some hidden files / folders with configuration

        os.mkdir(self.notebookDir)
        os.mkdir(self.pipelinesDir)

        self._createTestFiles()
    def _createTestFiles(self):

        ## notebook:
        content = {'notebookName': 'testNotebook',
                   'cellContents': [{'cellID': 'myWorkspace.myNotebookName.jfhfi4836',
                                    'cellType': 'code',
                                    'cellSyntax': 'python', # or Markdown, SQL, etc - little more generic than "language"
                                    'cellContent': 'a=5\nb=6\na+b'},
                                   {'cellID': 'myWorkspace.myNotebookName.fkao33k4n6',
                                    'cellType': 'code',
                                    'cellSyntax': 'python',  # or Markdown, SQL, etc - little more generic than "language"
                                    'cellContent': 'print("hello world! I am a second cell!")'}
                   ]}
        self.WriteNotebook('testNotebook.edpnb', content)

    def ReadNotebook(self, notebookFilename):

        path = os.path.join(self.notebookDir, notebookFilename)
        with open(path, 'r') as f:
            notebookContents = json.load(f)

        nb = Notebook(self, notebookContents)
        self.loadedNotebooks[nb.notebookName] = nb

        return nb


    def WriteNotebook(self, notebookFilename, content):

        path = os.path.join(self.notebookDir, notebookFilename)
        with open(path, 'w') as f:
            json.dump(content, f, indent=2)


    def WriteCell(self, notebookFilename, cellNum, cellContent):
        """
        Only write back a single cell
        """






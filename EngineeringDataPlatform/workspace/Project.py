
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

    def pathInProjecttoAbsolutePath(self, pathInProject):
        return os.path.join(self.projectDir, pathInProject)
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
        self.NotebookSaveOrSaveAs('testNotebook.edpnb', 'testNotebook', content)

    def NotebookRead(self, pathInProject):

        #path = os.path.join(self.notebookDir, notebookFilename)
        absPath = self.pathInProjecttoAbsolutePath(pathInProject)
        with open(absPath, 'r') as f:
            notebookContents = json.load(f)

        nb = Notebook(self, notebookContents, pathInProject=pathInProject)
        self.loadedNotebooks[nb.notebookName] = nb

        return nb

    def NotebookRename(self, previousName, newName):
        pass

    def NotebookSaveOrSaveAs(self, pathOnDisk, name, content):
        """
        update the content of an existing notebook, or figure out where it's going if we're saving it somewhere else
        """

        if name in self.loadedNotebooks and self.loadedNotebooks[name].pathInProject == pathOnDisk:
            self.NotebookSave(name, content)

        else:
            raise NotImplementedError('saving to new paths not implemented yet')

    def NotebookSave(self, name, content):
        # do we presumably already have this notebook loaded?
        # we could have changed the name though
        # no lets assume this is just a basic SAVE operation
        self.loadedNotebooks[name].updateContent(content)
        self.loadedNotebooks[name].save()

    # def WriteNotebook(self, notebookFilename, content):
    #
    #     path = os.path.join(self.notebookDir, notebookFilename)
    #     with open(path, 'w') as f:
    #         json.dump(content, f, indent=2)
    #
    #
    # def WriteCell(self, notebookFilename, cellNum, cellContent):
    #     """
    #     Only write back a single cell
    #     """






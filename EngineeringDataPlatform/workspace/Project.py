
"""
Do whatever folder creation and environment setup we need to do on the local disk
so that we can start getting persistent files.
"""

import os
import json
class Project:

    def __init__(self, localProjectSpaceDir, projectName):

        if localProjectSpaceDir[0] == '~':
            localProjectSpaceDir = localProjectSpaceDir.replace('~', os.path.expanduser('~').replace('\\', '/'))

        self.projectDir = os.path.join(localProjectSpaceDir, projectName)

        self.notebookDir = os.path.join(self.projectDir, 'notebooks')
        self.pipelinesDir = os.path.join(self.projectDir, 'pipelines')

        if not os.path.isdir(self.projectDir):
            # need to create whatever folder structure we need
            self._createEmptyProject()

    def _createEmptyProject(self):

        os.makedirs(self.projectDir)

        # what else do we need in here?
        # probably some hidden files / folders with configuration

        os.mkdir(self.notebookDir)
        os.mkdir(self.pipelinesDir)


    def ReadNotebook(self, notebookFilename):

        path = os.path.join(self.notebookDir, notebookFilename)
        with open(path, 'r') as f:
            return json.load(f)

    def WriteNotebook(self, notebookFilename, content):

        path = os.path.join(self.notebookDir, notebookFilename)
        with open(path, 'w') as f:
            json.dump(content, f, indent=2)


    def WriteCell(self, notebookFilename, cellNum, cellContent):
        """
        Only write back a single cell
        """






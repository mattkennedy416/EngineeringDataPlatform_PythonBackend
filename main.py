from flask import Flask, request, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


import queue
from jupyter_client.manager import start_new_kernel
from pprint import PrettyPrinter


from CodeExecution.RuntimeTest import RuntimeTest
from EngineeringDataPlatform.codingUtilities.notebookCellParser import NotebookCellParser

from EngineeringDataPlatform import workspace

localProjectSpace = "~/Documents/EngineeringDataPlatform/ProjectSpace/"

project = workspace.Project(localProjectSpace, 'testProject')


runtime = RuntimeTest()


@app.route("/", methods=['GET', 'POST'])
def hello_world():

    """
    from postman:
    - body, raw, json format
    - {"code": "10 + 5"}
    :return:
    """

    #code = request.args.get('code')
    content = request.json
    if 'code' in content:
        code = content['code']
        if isinstance(code, list): # coming from javascript we get [str] rather than str
            code = ' '.join(code) # it'll pass spaces as different parameters
        interpreter_response, environmentVariables = runtime.Execute(code)

        parseForAdditionalInfo = NotebookCellParser(code)
        for symbol in parseForAdditionalInfo.symbols:
            if symbol in environmentVariables: # so we seem to have lost our type data here... that's a problem
                pass
    else:

        interpreter_response, environmentVariables = "no code parameter received", None


    queryResponse = {'type': 'json',
                     'status': {'state': 'success',
                                'msg': ''},
                     'output': ''}

    if 'msg' in interpreter_response['info'] and interpreter_response['info']['msg_type'] == 'error':
        queryResponse['status']['state'] = 'error'
        queryResponse['status']['msg'] = interpreter_response['info']['msg']

    if interpreter_response['data'] is not None and 'text/plain' in interpreter_response['data']:
        queryResponse['output'] = interpreter_response['data']['text/plain']

    # we can probably figure out how to send back only what's changed
    queryResponse['environment'] = environmentVariables

    #return json.dumps(queryResponse)
    return jsonify(queryResponse)

#
@app.route("/repo_dir/", methods=['POST', 'GET'])
def file_tree_viewer():
    """
    let the file tree viewer to get a directory structure
    :return:
    """

    structure = {'name': 'root',
                 'checked': 0,
                 'isOpen': True,
                 'children': [
                     {'name': 'child 1', 'checked': 0},
                     {'name': 'child 2', 'checked': 0},
                 ]}

    return json.dumps(structure)


@app.route("/etl/load_csv/", methods=['POST'])
def etl_load_csv():
    """
    Load in a csv from disk specified by filename in the parameters

    url: 127.0.0.1:5000/etl/load_csv/
    body -> raw -> JSON:
    {"filepath": "E:/Projects/DataPlatform/TestData/mhnc.us.txt",
    "etl_type": "LoadSingle_Local"}

    :return:
    """

    filepath = request.json.get('filepath')
    #varName = request.json.get('varname')

    # if varName is None:
    #     varName = os.path.split(filepath)[1].replace('.', '_').replace('\\', '_').replace('/', '_')

    # if filepath is not None:
    #     #imports = 'import BEH\n'
    #     runtime.Execute(varName + ' = BEH.ETL.etl_load_csv("' + filepath + '")')

    # config = {'etl_type': 'LoadSingle_Local',
    #           'filepath': 'E:/Projects/DataPlatform/TestData/mhnc.us.txt'}
    config = request.json
    runtime.ETL_Load_CSV(config)

    return 'loaded'


@app.route('/workspace/hello', methods=['POST'])
def WorkspaceHelloWorld():
    """
    can we ping the backend workspace services?
    """

    return {'message': 'hello!'}


@app.route('/workspace/notebooks', methods=['POST', 'GET'])
def WorkspaceNotebookFiles():
    """
    Workspace Notebook File operations such as reading, writing, searching, permissions, and more

    This is not executing code within notebooks.
    """

    # workspace = request.json.get('workspace', None)
    # filename = request.json.get('filename', None)
    # cells = request.json.get('cells', [])


    if request.method == 'GET':
        pathInProject = request.args.get('notebookPath')

        notebook = project.NotebookRead(pathInProject)

        # # lets do a read all cells operation:

        return notebook.toJSON()

    elif request.method == 'POST':
        pathOnDisk = request.json.get('notebookPath')
        name = request.json.get('notebookName')
        content = request.json.get('content')
        #project.WriteNotebook(filename, content)
        project.NotebookSaveOrSaveAs(pathOnDisk, name, content)

        return 'success'

@app.route('/workspace/notebooks/execute', methods=['POST'])
def NotebooksExecute():
    """
    handle code execution of notebook cells

    lets treat this the same way we treat a partial notebook save operation,
    but do a save + execute after
    """

    name = request.json.get('notebookName')
    content = request.json.get('cellContent')

    if isinstance(content, dict):
        content = [content]

    queryResponse = project.NotebookCellExecution(name, content)
    return jsonify(queryResponse)


# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run()



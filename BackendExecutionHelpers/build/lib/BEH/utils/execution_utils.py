

import json
import inspect

def cleanEnvironmentVars(varDict):
    output = {}
    for key in varDict:
        print('processing key', key)
        if inspect.ismodule(varDict[key]):
            continue

        if key[0] != '_' and key not in ['In', 'Out', 'get_ipython', 'exit', 'quit']:
            #print('including key in output environment variables', key)
            output[key] = {'val': str(varDict[key]), 'type': str(type(varDict[key]))[8:-2]} # remove the "<class '" and "'>"
            #output[key] = str(varDict[key])
        else:
            #print('Filtering env var as hidden:', key)
            continue

    return json.dumps(output)


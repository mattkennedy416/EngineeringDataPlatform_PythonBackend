

import json

def cleanEnvironmentVars(varDict):
    output = {}
    for key in varDict:
        print('processing key', key)
        if key[0] != '_' and key not in ['In', 'Out', 'get_ipython', 'exit', 'quit']:
            print('including key in output environment variables', key)
            output[key] = str(varDict[key])
        else:
            print('Filtering env var as hidden:', key)

    return json.dumps(output)




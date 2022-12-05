
import json
import jupyter_client

class RuntimeTest:

    def __init__(self):


        self.kernel_manager = jupyter_client.KernelManager()

        self.kernel_manager.start_kernel()

        self.client = self.kernel_manager.blocking_client()
        self.client.start_channels()

        #self._inject_functions_and_files()


    # def _inject_functions_and_files(self):
    #     # as an interim alternative to building and importing packages to the ipython kernel, lets just directly inject the code we need
    #     with open('./ETL/ETL_CSV.py', 'r') as f:
    #         code = f.read()
    #         self._execute_code_blocking(None, code)

        initialization_code = "import BEH\n" \
                              "__dataManager = BEH.Workspaces.Workspaces()\n" \
                              "__etlManager = BEH.ETL.ETLManager(__dataManager)"
        self._execute_code_blocking(None, initialization_code) # <- import our backend tools

    def _get_defined_variables(self, interpreter_id):
        """
        Get the local and global variables in an already running interpreter.
        :param interpreter_id:
        :return:
        """
        #code = "locals() | globals()"
        #code = "vars()"
        # code = "def _cleanEnvironmentVars(varDict):\n" \
        #        "    #allVars = locals() | globals()\n" \
        #        "    output = {}\n" \
        #        "    for key in varDict:\n" \
        #        "        if key[0] != '_' and key not in ['In', 'Out', 'get_ipython', 'exit', 'quit']:" \
        #        "            output[key] = str(varDict[key])\n" \
        #        "    import json\n" \
        #        "    return json.dumps(output)"
        # self._execute_code_blocking(interpreter_id, code)
        varsText = self._execute_code_blocking(interpreter_id, "BEH.utils.cleanEnvironmentVars(vars())")

        # also windows filepaths will cause an error with their \ vs /
        variables = json.loads(varsText['data']['text/plain'][1:-1].replace('\\', '/')) # for some reason this is like a double string with double quotes around the single quotes? remove the single quotes so we can parse this into a dictionary

        print(variables)
        return variables



    def _execute_code_blocking(self, interpreter_id, code):
        """
        Execute newly received code in an already running interpreter and wait until we get a result
        :param interpreter_id:
        :param code:
        :return:
        """
        msg_id = self.client.execute(code)
        info = {}

        while True:
            # so the content is returned in iopub, and it goes through a few different stages from reply -> starting -> busy -> result
            reply_ui = self.client.get_iopub_msg()
            if reply_ui['msg_type'] == 'execute_result' and reply_ui['parent_header']['msg_id'] == msg_id: # there is a return ( 5 + 10 )
                break
            elif reply_ui['msg_type'] == 'status' and reply_ui['content']['execution_state'] == 'idle' and reply_ui['parent_header']['msg_id'] == msg_id: # there is no return ( a + 12 )
                break
            elif reply_ui['msg_type'] == 'error':
                info['msg_type'] = 'error'
                info['msg'] = reply_ui['content'].get('evalue')
                break

        # so reply_ui is getting the string-wrapped version for printing to the UI... that's not really what we want internally here
        response = {'data': reply_ui['content'].get('data'),
                    'info': info}
        return response


    def Execute(self, code):
        print('received code:', code)

        interpreter_id = 0
        interpreter_response = self._execute_code_blocking(interpreter_id, code)

        if not ('msg_type' in interpreter_response['info'] and interpreter_response['info']['msg_type'] == 'error'):
            self._get_defined_variables(interpreter_id)

        return interpreter_response


    def ETL_Load_CSV(self, config):
        """
        Get the configuration and pass it to the ETL Manager running in the Kernel
        :param config:
        :return:
        """

        # configStr = "{'etl_type': 'LoadSingle_Local'," \
        #             "'filepath': 'E:/Projects/DataPlatform/TestData/mhnc.us.txt'}"

        code = "__etlManager.New_ETL_FromConfig(" + str(config) + ")\n" \
                "__etlManager.ComputeCycle()" # <- just force it to run right away

        self._execute_code_blocking(None, code)



"""
As an interim solution this file in its entirety is getting directly injected into IPython environments
"""


import numpy as np
import pandas as pd
import glob
import random
import os

from BEH.ETL.ETL_Item import ETLItem

class ETL_CSV(ETLItem):

    def __init__(self, config):
        super().__init__(config)

        self.available_item_types = {'LoadSingle_Local': self.local_load_single,
                                     'LoadFolder_Local': self.local_load_folder}


    def local_load_single(self):
        """
        config = {"etl_type": "LoadSingle_Local",
                  "filepath": str - required
                  "skip_header_rows": int - default: 0
                  "load_max_rows": int - default: None (no limit)
                  "custom_transform_function": python_code_string
                  "custom_transform_function_name": string; name of def/function
                  }

        for the custom_transform_function, I think we'll need to execute this as a function, but we need to know the function name in here
        - should assume that the only input is self.config, but I suppose they can pass whatever additional info they want in there, right?
        - the return will be assigned to our data output, if there are multiple returns it'll be a tuple

        Example custom pipeline:
        def CustomTransform12345(etl_params):
            path = etl_params['filepath']
            lines = []
            with open(path, 'r') as f:
                for line in f:
                    lines.append(line.split(','))
            return lines

        :param config:
        :return:
        """

        filepath = self.config.get('filepath')
        skip_header_rows = self.config.get('skip_header_rows', 0)
        load_max_rows = self.config.get('load_max_rows', None)

        custom_transform_code = self.config.get('custom_transform_function', None)
        function_name = self.config.get('custom_transform_function_name', None)
        if custom_transform_code is not None:
            try:
                exec(custom_transform_code)
                data = eval(function_name+"(" + str(self.config) + ")")
            except:
                raise ChildProcessError('Custom Transform Function failed ')

        else:
            data = pd.read_csv(filepath, skiprows=skip_header_rows, nrows=load_max_rows)

        varName = os.path.split(filepath)[1].replace('.','_')

        self.output = {varName: data}
        self.complete_this_etl() # once and done

        # don't return the data from here it's a mess getting it back to the user's workspace, get is passed to the data manager instead?



    def local_load_folder(self):
        """
        config = {"etl_type": "LoadFolder_Local",
                    "directory": str - required,
                    "max_files": int - default: None (no limit),
                    "randomize_load_order": bool - default False <- eg randomize+max_files would give you different files every time
                    "recursive": bool - default: False,
                    "filename_contains_substr": str - rather than a regex match lets do an easy substring match,
                    "filename_regex_match": str - regex match on the filename,
                    "skip_header_rows": int - default: 0
                    "load_max_rows": int - default: None (no limit)
                    }

        might also need some details / config on how to load individual files, but lets not worry about that for now
        such as if we have a weird file format that's text and not actually CSV or non-comma delims?
        maybe split that out into a ETL_TXT that has more support for weird stuff
        ALSO - can we somehow create custom loaders through a no/low-code ui?

        :param config:
        :return:
        """

        directory = self.config.get('directory')
        max_files = self.config.get('max_files', None)
        randomize_load_order = self.config.get('randomize_load_order', False)
        recursive = self.config.get('recursive', False)
        filename_contains_substr = self.config.get('filename_contains_substr', None)
        filename_regex_match = self.config.get('filename_regex_match', None)
        skip_header_rows = self.config.get('skip_header_rows', 0)
        load_max_rows = self.config.get('load_max_rows', None)

        custom_transform_code = self.config.get('custom_transform_function', None)
        function_name = self.config.get('custom_transform_function_name', None)

        if custom_transform_code is not None:
            try:
                exec(custom_transform_code)
            except:
                raise ChildProcessError('Custom Transform Function failed ')


        loaded_files = {}

        paths = glob.glob(directory + '/*') # don't worry about recursive yet

        if randomize_load_order:
            random.shuffle(paths) # should be an in-place operation

        for n in range(len(paths)):
            filename = os.path.split(paths[n])[1]

            # lets do our negative cases
            if filename_contains_substr is not None and filename_contains_substr not in filename:
                continue
            if filename_regex_match is not None:
                raise NotImplementedError("regex filename matching is not yet implemented, don't pass this parameter")

            # alright we want this file!
            if custom_transform_code is not None:
                try:
                    # lets pass a second a parameter here for config + current path
                    data = eval(function_name + "(" + str(self.config) + ", '" + str(paths[n]).replace('\\', '/') + "')")
                except:
                    raise ChildProcessError('Custom Transform Function failed ')
            else:
                data = pd.read_csv(paths[n], skiprows=skip_header_rows, nrows=load_max_rows)

            relPath = paths[n].replace(directory, '').replace('.','_') # <- won't work in all cases but good enough temporary solution
            if relPath[0] in ['/', '\\']:
                relPath = relPath[1:] # cut this off so we start like "subdir/file" not "/subdir/file"

            loaded_files[relPath] = data # <- if we're doing recursive load we can have multiple files with the same name

            if max_files is not None and len(loaded_files) >= max_files:
                break

        self.output = loaded_files
        self.complete_this_etl()  # once and done








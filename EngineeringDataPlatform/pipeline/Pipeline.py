


# def ETLWrapper(func):
#
#     def execute(*args, **kwargs):
#         return func(*args, **kwargs)
#
#     return execute


import numpy as np
import pandas as pd




class Pipeline:

    def __init__(self, steps_list, workspace):
        self.steps_list = steps_list
        self.steps_indexed = {}
        self.workspace = workspace

        for step in self.steps_list:
            step.assign_to_pipeline(self, self.workspace)
            self.steps_indexed[step.item_name] = step

        self.run_num = -1

    def execute(self):
        self.run_num += 1

        for n, step in enumerate(self.steps_list):
            step.execute()

        return self




class PipelineItem:
    def __init__(self, func, config):
        self.func = func
        self.config = config
        self.results = None
        self.item_name = config.get('name')
        self.inputs = config.get('inputs')
        self.pipeline = None
        self.workspace = None
        self.run_num = 0

    def assign_to_pipeline(self, pipeline, workspace):
        self.pipeline = pipeline
        self.workspace = workspace
        self.config['_workspace'] = workspace
        self.config['_pipeline'] = pipeline

    def execute(self):

        inputs = self.get_inputs()
        if inputs is None:
            self.results = self.func(self.config)
        else:
            self.results = self.func(self.config, *inputs)

        self.run_num = self.pipeline.run_num # so we can check if this item has been updated yet this iteration


    def get_inputs(self):
        input_steps = []
        if self.inputs is not None:
            if isinstance(self.inputs, str):
                self.inputs = [self.inputs]
            for input_step_name in self.inputs:
                input_steps.append(self.pipeline.steps_indexed[input_step_name])

            # need to check if they're up to date, but that validation should be happening before we get to here
            inputs = [i.results for i in input_steps]
            return inputs
        else:
            return None



if __name__ == '__main__':
    a = PipelineItem(extract_example, {'name': 'extract_example', 'inputs': None})
    b = PipelineItem(transform_example, {'name': 'transform_example', 'inputs': ['extract_example'], 'multiplyBy': 3})
    c = PipelineItem(load_example, {'name': 'load_example', 'inputs': ['transform_example']})

    p = Pipeline([a,b,c]).execute()


    # ok I think this structure will be good enough for linear ingests
    # what are the next steps that we need here?
    # - associate a pipeline with a workspace so it has the context
    # - store the history of the pipeline being run so we can lookup if the inputs have changed
    # - maybe hook-up that watchfile library

    # how do we want to handle more complicated graphs?
    # - should just need to specify the parents, ie that the inputs have been calculated, and then children?






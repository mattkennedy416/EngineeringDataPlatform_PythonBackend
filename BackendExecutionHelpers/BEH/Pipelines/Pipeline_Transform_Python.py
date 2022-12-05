

from BEH.Pipelines.Pipeline_Item import PipelineItem


class Pipeline_Transform_Python(PipelineItem):

    def __init__(self, config, dataManager):
        super().__init__(config, dataManager)

        self.available_item_types = {'PythonTransform': self.python_transform}


    def python_transform(self):
        """
        need to get the inputs and any dependencies in here right? and then execute our code?

        execute in a generated function like:

        def myTransformFunction(input1, input2, ...):
            *inject pipeline code*

        myTransformFunction(input1.output, input2.output, ...)

        :return:
        """
        inputObjects = self.pipeline.get_input_objects(self.input_item_names)

        code = self.config['pipeline_item_type_config']['code']
        codeIndented = '\n'.join(['    ' + line for line in code.split('\n')])

        transformName = self.get_name()
        inputNames = ','.join([obj.get_name() for obj in inputObjects])
        callNames = ','.join(["inputObjects[" + str(n) + "].output" for n in range(len(inputObjects))])

        # need to make sure we're correctly indented, but don't worry too much about that now
        transformCode = "def " + transformName + "(" + inputNames + "):\n" + codeIndented
                         #"__dataManager.add_data_to_namespace({'" + transformName + "': " + transformName + "(" + callNames + ")})"

        # note that this isn't safe from abuse ( eg quit() )but we should only be executing user-written code in separate IPython Kernels from the main thread
        # if they crash it they just crash the kernel and I guess they get to restart it, this shouldn't impact the actual front or backend
        exec(transformCode) # <-- define the function
        self.output = eval(transformName + "(" + callNames + ")") # and evaluate the function, passing the outputs from our defined input Pipeline items





class Pipeline:

    def __init__(self):

        self.pipeline_items = {}


    def add_item(self, pipelineItem):

        self.pipeline_items[pipelineItem.get_name()] = pipelineItem
        pipelineItem.add_to_pipeline(self)


    def get_input_objects(self, inputNames):
        inputObjects = []
        for name in inputNames:
            if name in self.pipeline_items:
                inputObjects.append(self.pipeline_items[name])

        return inputObjects




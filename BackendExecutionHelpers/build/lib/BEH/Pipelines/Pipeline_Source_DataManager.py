

from BEH.Pipelines.Pipeline_Item import PipelineItem


class PipelineSource_DataManager(PipelineItem):

    def __init__(self, config, dataManager):
        super().__init__(config, dataManager)

        self.available_item_types = {'DataManagerSource': self.data_manager_source}



    def data_manager_source(self):
        """
        we want to set our output to be a copy of the object from the data manager
        :return:
        """

        typeConfig = self.config.get('pipeline_item_type_config')
        dataManagerName = typeConfig['DataManagerName']

        self.output = self.data_manager.get_data_by_name(dataManagerName)


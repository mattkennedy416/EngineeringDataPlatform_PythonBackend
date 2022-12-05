
import uuid

class PipelineItem:
    """
    A pipeline item should represent a single table, transformation, evaluation of a model, writing to a database, etc
    it can have multiple input connections but should likely be scoped to have a single output

    outputs are not necessarily pushed anywhere but rather pulled by another action.

    should be able to be fully defined by and imported/exported to JSON files
    """

    def __init__(self, config, dataManager):

        #possible_item_types = ['DataManagerSource', 'PythonTransform']

        self.uuid = uuid.uuid1()
        self.data_manager = dataManager

        self.available_item_types = {}

        self.config = config

        self.pipeline_item_unique_name = config.get("pipeline_item_unique_name", None)
        self.pipeline_item_type = config.get('pipeline_item_type', None)
        self.pipeline_item_type_config = config.get('pipeline_item_type_config', {})

        self.input_item_names = self.pipeline_item_type_config.get('input_item_names', [])
        self.code = self.pipeline_item_type_config.get('code', {}) # include language, format, actual functions, etc, what environment we're running in?

        self.output = None # can we get this to a single value / object? or really it'll be a single input to another pipeline item
        self.isCompleted = False
        self.pipeline = None

    def execute(self):
        self.available_item_types[self.get_pipeline_item_type()]()
        self.isCompleted = True

    def add_to_pipeline(self, pipeline):
        self.pipeline = pipeline
    def get_pipeline_item_type(self):
        return self.config.get('pipeline_item_type')

    def get_uuid(self):
        return uuid

    def get_name(self):
        return self.config.get('pipeline_item_unique_name')

    def is_completed(self):
        return self.isCompleted

    def has_output(self):
        return self.output is not None

    def get_output(self):
        return self.output

    def throw_warning(self, message, from_input_items=None):
        """
        how would we pass something back to the UI from here?
        might need to run some kind of validation check as they're being written / defined?

        from_input_items is the incoming paths/connections that should be flagged as having an issue

        **use this when something might be a problem but we can probably attempt to execute**
        :param message:
        :return:
        """

        print('warning thrown to UI!', message)

    def throw_error(self, message, from_input_items=None):
        """
        how would we pass something back to the UI from here?
        might need to run some kind of validation check as they're being written / defined?

        from_input_items is the incoming paths/connections that should be flagged as having an issue

        **use this when we cannot execute, such as data type incompatibilities between inputs/outputs**
        :param message:
        :return:
        """
        print('error thrown to UI!', message)

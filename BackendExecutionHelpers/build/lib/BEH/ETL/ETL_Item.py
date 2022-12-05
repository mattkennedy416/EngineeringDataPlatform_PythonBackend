


import uuid


class ETLItem:

    def __init__(self, config):

        self.uuid = uuid.uuid1()

        self.available_item_types = {}

        self.config = config
        self.isCompleted = False
        self.etlManager = None

        self.isRepeating = False

        self.output = None # <- I guess use this as our universal return? as well as storing stuff historically? don't necessarily want two copies though


    def __eq__(self, other):
        otherID = None
        try:
            otherID = other.get_uuid()
        except:
            return False

        if otherID == self.get_uuid():
            return True
        else:
            return False


    def get_namespace(self):
        # override by subclassed item?
        return self.config.get('namespace', self.etlManager.get_default_namespace())

    def get_varname(self):
        # override by subclassed item?
        return self.config.get('varname', self.get_uuid())

    def get_uuid(self):
        return uuid

    def can_run_next_cycle(self):
        if self.isCompleted:
            return False # what are we doing here? no!

        if not self.isRepeating:
            return True # one and done that's still in the queue
        else:
            return False # worry about the timing stuff later

    def execute(self):
        if self.can_run_next_cycle():

            # run our ETL operation which should
            self.available_item_types[self.get_etl_type()]()



    def get_etl_type(self):
        return self.config.get('etl_type')


    def complete_this_etl(self):
        """
        This ETL Item will be marked as completed and no more compute will be spent on it, though we can keep it in the history
        :return:
        """
        self.isCompleted = True

    def is_completed(self):
        return self.isCompleted

    def get_output(self):
        return self.output

    def has_output(self):
        return self.output is not None


    def add_to_manager(self, etlManager):
        """
        This ETL item is being picked up by an ETL Manager for compute cycles
        :param etlManager:
        :return:
        """
        self.etlManager = etlManager







#from ETL_Item import ETLItem
from BEH.ETL.ETL_CSV import ETL_CSV


class ETLManager:

    def __init__(self, dataManager):

        self.data_manager = dataManager

        # need to index available item types to the appropriate loader object
        available_loader_classes = [ETL_CSV] # <-- ADD NEW LOADERS TO THIS LIST
        self.etl_type_to_class = {}
        for c in available_loader_classes:
            etl_types = c({}).available_item_types.keys()
            for etype in etl_types:
                self.etl_type_to_class[etype] = c


        self.all_etl_inProgress_items = []
        self.all_etl_completed_items = []

    def get_default_namespace(self):
        return self.data_manager.get_default_namespace()

    def ComputeCycle(self):
        """
        lets do the minimum amount of work possible to accomplish something
        eg load a single CSV even if there's 25 CSVs in our queue
        :return:
        """
        for item in self.all_etl_inProgress_items:

            item.execute()
            # we're going to have issues here with the list changing size as items complete...
            if item.is_completed() and item.has_output():
                self.data_manager.add_data_to_namespace(item.get_output(), namespace=item.get_namespace())

        # move completed items out of the in-progress queue
        n = 0
        while n < len(self.all_etl_inProgress_items):
            if self.all_etl_inProgress_items[n].is_completed():
                self.all_etl_completed_items.append(self.all_etl_inProgress_items[n])
                del self.all_etl_inProgress_items[n] # remove this item from in-progress list
            else:
                n += 1


    def New_ETL_FromItem(self, ETLItem):

        ETLItem.add_to_manager(self)
        self.all_etl_inProgress_items.append(ETLItem)


    def New_ETL_FromConfig(self, ETLConfig):
        etl_type = ETLConfig.get('etl_type')
        if etl_type in self.etl_type_to_class:
            etlItem = self.etl_type_to_class[etl_type](ETLConfig)
            self.New_ETL_FromItem(etlItem)

        else:
            #print('ETL Type not associated with an imported class:', etl_type)
            raise ValueError('ETL Type not associated with an imported class: ' + str(etl_type))





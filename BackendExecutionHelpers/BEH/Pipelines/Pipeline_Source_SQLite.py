

from BEH.Pipelines.Pipeline_Item import PipelineItem
import pandas as pd
import sqlite3

"""
We'll need to figure out if we can do a somewhat common interface for interfacing with SQL databases
eg we want to be able to change the backing database infrastructure and the user to not notice or care, 
including any configuration they see

so they likely shouldn't be creating a SQLite pipeline item vs a PostgreSQL pipeline item, etc

but worry about that later after we're compatible with multiple backends
"""



class Pipeline_Source_SQLite(PipelineItem):

    def __init__(self, config, dataManager):
        super().__init__(config, dataManager)

        self.available_item_types = {'ReadFromSQLite': self.read_from_sqlite,
                                     'WriteToSQLite': self.write_to_sqllite}


    def read_from_sqlite(self):
        """
        read the specified table from the specified database
        :return:
        """

        # pd.read_sql('SELECT * FROM test_sqlite_stock_data', conn)

        table_name = self.pipeline_item_type_config['table']
        dbConnection = self.pipeline_item_type_config['db']

        conn = sqlite3.connect(dbConnection['address'])

        self.output = pd.read_sql('SELECT * FROM ' + table_name, conn, index_col='index')


    def write_to_sqllite(self):
        """
        output from this should be the connection info to read it back
        :return:
        """

        inputObjects = self.pipeline.get_input_objects(self.input_item_names)

        # we're going to be more picky on the formats we can accept here
        # can we define like a pipeline warning and a pipeline error method?
        for item in inputObjects:
            if not isinstance(item.output, pd.DataFrame):
                self.throw_error("Write to SQLite: incompatible input " + item.get_name() + " is of type " + str(type(item.output)), from_input_items=[item])
                return # since an error is saying we can't continue

        # dbConnection = {'type': 'sqlite',
        #                 'address': 'pythonsqlite.db'}
        dbConnection = self.pipeline_item_type_config['db']
        conn = sqlite3.connect(dbConnection['address'])

        if 'output_table_names' in self.pipeline_item_type_config:
            output_table_names = self.pipeline_item_type_config['output_table_names']
        else:
            output_table_names = {}

        for item in inputObjects:

            if item.get_name() in output_table_names:
                # if provided, pull the table name from the pipeline configuration
                tableName = output_table_names[item.get_name()]
            else:
                tableName = item.get_name()
                output_table_names[item.get_name()] = item.get_name()

            item.output.to_sql(tableName, conn, if_exists="replace")

        self.output = {'db': dbConnection,
                        'table_names': output_table_names}




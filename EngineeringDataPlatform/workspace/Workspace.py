
import uuid
import sqlparse
import pandas as pd
from EngineeringDataPlatform.table.Table import Table

import warnings

class Workspace:

    def __init__(self, name, engine, dbname):
        self._name = name
        self._engine = engine
        self._uid = uuid.uuid1()
        self._tables_in_memory = []

        self._database_name = name

        self.workspace_port_offset = 1


    def __eq__(self, other):
        if isinstance(other, Workspace) and other._uid == self._uid:
            return True
        else:
            return False

    def get_workspace_port_offset_for_local_containers(self):
        return self.workspace_port_offset

    def engine(self):
        return self._engine

    def name(self):
        return self._name

    def add(self, table):

        # lets check if this table already exists in the workspace and throw a warning if so
        for t in self._tables_in_memory:
            if table.equals_approx(t) and table.name() == t.name():
                warnings.warn('A table with the same schema and name (' + table.name() + ') is already loaded in this workspace, '
                              'loading it again but check your code. Lookup may not work as expected.')
                break

        self._tables_in_memory.append(table)

    def remove_table(self, table):
        for n in range(len(self._tables_in_memory)):
            if table.equals_approx(self._tables_in_memory[n]) and table.name() == self._tables_in_memory[n].name():
                del self._tables_in_memory[n]
                break

    def sql(self, sql):
        # execute SQL against the database
        print('execute sql statement')

        with self.engine().begin() as con:
            dfresults = pd.read_sql(sql, con)
        tresults = Table(dfresults)
        tresults.initialize(self, self.generate_new_table_name(from_sql_statement=sql))
        return tresults

    def load_table_from_database(self, name):
        # there's probably a better way to do this, but lets just run a sql statement for now
        sql = 'SELECT * FROM ' + name
        table = self.sql(sql)

        # set the index as index
        if 'index' in table.columns.values:
            table.set_index('index', drop=True, inplace=True)

        # except we want to override the newly generated / derived tablename
        table.initialize(self, name)

        return table


    def generate_new_table_name(self, from_sql_statement=None):
        if from_sql_statement is None:
            return 'new_table'

        elif 'from' in from_sql_statement.lower() and 'where' in from_sql_statement.lower():
            start = from_sql_statement.lower().find('from') + len('from')
            end = from_sql_statement.lower().find('where')
            base_table_name = from_sql_statement[start:end].strip()
            return base_table_name+'_1'

        elif 'from' in from_sql_statement.lower():
            start = from_sql_statement.lower().find('from') + len('from')
            base_table_name = from_sql_statement[start:].strip()
            return base_table_name + '_1'

        else:
            return 'unhandled_table_case'

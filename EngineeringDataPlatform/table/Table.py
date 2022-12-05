
import pandas as pd
import numpy as np

class Series(pd.Series):

    @property
    def _constructor(self):
        return Series

    @property
    def _constructor_expanddim(self):
        return Table



class Table(pd.DataFrame):


    _metadata = ['_database_name', '_table_name', '_workspace', '_has_been_initialized'] # property will be passed to manipulation results

    def workspace(self):
        return self._workspace

    def name(self):
        return self._table_name

    def equals_approx(self, other):
        # a fast equals looking at the meta-data rather than all the actual values
        if not isinstance(other, Table):
            return False
        if not np.array_equal(other.columns.values, self.columns.values):
            return False
        if not np.array_equal(other.dtypes, self.dtypes):
            return False

        if other.shape != self.shape:
            return False # <- this may get more complicated when we're not loading everything

        return True

    def commit(self, if_exists='replace'):
        """
        Write table contents to database

        :param if_exists: {'fail','replace','append'}
        :return:
        """
        try:
            self.to_sql(self.name(), self.workspace().engine(), method='multi', if_exists=if_exists)
            return True
        except:
            return False


    def load_sample(self, num_rows=250):
        # load the first num_rows from the backing table
        print('load sample!')

    def sql(self, sql):
        # execute SQL against the database
        print('execute sql statement')

        # lets actually move all of this to the workspace level for full SQL statements against the workspace/database
        return self.workspace().sql(sql)

    def select_where(self, sql_where, return_cols=None):
        """
        Lets allow a shortcut when executing against the table for filtering
        :param sql_where:
        :return:
        """
        if return_cols is not None:
            col_str = '(' + ','.join(return_cols) + ')'
        else:
            col_str = '*'

        sql = 'SELECT ' + col_str + ' from ' + self.name() + ' WHERE ' + sql_where
        return self.workspace().sql(sql)

    def initialize(self, workspace, table_name):

        if '_has_been_initialized' in self.__dict__: # don't add it to the environment twice if we're moving or resetting stuff
            self.workspace().remove_table(self)

        self._workspace = workspace
        self._table_name = table_name

        self._workspace.add(self) # register yourself with the workspace
        self.__dict__['_has_been_initialized'] = True


    @property
    def _constructor(self):
        return Table

    @property
    def _constructor_sliced(self):
        return Series
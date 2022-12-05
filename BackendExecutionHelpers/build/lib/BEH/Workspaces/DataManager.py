

import pickle
import copy

class DataManager:

    def __init__(self):

        self._data = {}
        self.default_namespace = 'default_namespace'

    def get_default_namespace(self):
        return self.default_namespace

    def create_namespace(self, namespace):
        if namespace in self._data:
            # do nothing?
            pass
        else:
            self._data[namespace] = {}


    def if_namespace_exists(self, namespace):
        if namespace in self._data:
            return True
        else:
            return False


    def get_available_namespaces(self):
        return list(self._data.keys())

    def add_data_to_namespace(self, dataDict, namespace=None):
        """
        add a dictionary of {varname: datavalue} to the data dictionary

        this is actually our new standard, the varname is generated by the loaded

        :param namespace:
        :param dataDict:
        :return:
        """
        if namespace is None:
            namespace = self.get_default_namespace()

        if not self.if_namespace_exists(namespace):
            self.create_namespace(namespace)

        self._data[namespace].update(dataDict)

    def get_data_by_name(self, name, namespace=None):
        """
        return a copy of the data object, otherwise transformations may be modifying in place
        :param name:
        :param namespace:
        :return:
        """
        if namespace is None:
            namespace = self.get_default_namespace()

        if namespace in self._data and name in self._data[namespace]:
            return copy.copy(self._data[namespace][name])






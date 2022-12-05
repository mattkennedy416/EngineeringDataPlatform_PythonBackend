




class Source:

    def __init__(self, source_name, config):

        self.config = config
        self.source_type = self.config.get('source_type')

        self._is_source_available = False
        self.source_name = source_name


    def connect(self):
        """
        establish a connection to this source so that data can be read
        :return:
        """

    def is_connected(self):
        pass

    def read(self, query):
        if not self.is_connected():
            raise SystemError('Not connected to source ' + self.source_name)


    def write(self, query):
        if not self.is_connected():
            raise SystemError('Not connected to source ' + self.source_name)


    def is_source_available(self):
        """
        for things like containers, we need to make sure they're started up before actually querying them.
        This function should be called every so often (eg 5-60 seconds) until we set self._is_source_available=True
        :return:
        """
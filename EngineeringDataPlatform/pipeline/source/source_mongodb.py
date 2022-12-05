
from EngineeringDataPlatform.pipeline.source.source import Source

import pymongo


class Source_MongoDB(Source):

    def __init__(self, source_name, source_env, workspace, credentials=None, read_only=True):
        """

        may determine how we do things like health checks and making sure we're up and ready:

        source_env = {'source_env': 'localhost_container',
                        'localhost_container': {'container_manager': WorkspaceContainerManager,
                                                'connection_url': 'mongodb://localhost',
                                                'container_ref': python_on_whales.Container,
                                                'container_config': {'image': 'mongo',
                                                                    'ports': [(27017, 27017)]}}}

        :param source_env: [str] {'localhost_application', 'localhost_container', 'remote_server'}
        :param credentials:
        :param read_only:
        """

        self.workspace = workspace

        self.source_type = 'database'
        self.source_name = source_name
        self.source_env = source_env

        self.connection_config = {'database_type': 'mongodb',
                                  'connection_url': self._getConnectionUrlFromSourceEnv(),
                                  'credentials': credentials,
                                  'read_only': read_only,
                                   'data_type': 'records'} # probably specify {records, tables} to do basic validations; eg can't push a pd.DataFrame to mongo without some transformations

        self.config = {'source_type': self.source_type,
                       'source_env': self.source_env,
                       self.source_type: self.connection_config,
                       self.source_name: self.source_name}

        super().__init__(self.source_name, self.config)

        self.client = None


    def _getConnectionUrlFromSourceEnv(self, include_port=True):

        connection_url = self.source_env[self.source_env['source_env']]['connection_url']

        if include_port:
            port_num = self._getPortFromSourceEnv()
            if port_num is not None:
                offset = self.workspace.get_workspace_port_offset_for_local_containers()
                port_str = ':' + str(port_num + offset)
                return connection_url + port_str

        return connection_url


    def _getPortFromSourceEnv(self):
        if self.source_env['source_env'] == 'localhost_container':
            return self.source_env[self.source_env['source_env']]['container_config']['ports'][0]
        else:
            return None


    def connect(self):
        connection_url = self._getConnectionUrlFromSourceEnv(include_port=True)
        credentials = self.connection_config['credentials']

        self.client = pymongo.MongoClient(connection_url) # example url = "mongodb://localhost:27017/"


    def is_connected(self):
        return self.client is not None


    def read(self, query):
        super().read(query)

        db_name = query.get('database_name')
        collection_name = query.get('collection')

        db = self.client[db_name]
        col = db[collection_name]

        results = col.find_one()
        return results


    def write(self, query):
        super().write(query)

        db_name = query.get('database_name')
        collection_name = query.get('collection')
        data = query.get('data')

        db = self.client[db_name]
        col = db[collection_name]

        results = col.insert_one(data)
        return results


    def is_source_available(self):
        """
        for things like containers, we need to make sure they're started up before actually querying them
        :return:
        """
        if self.source_env['source_env'] == 'localhost_container':

            # do we have a reference to the container?
            if self.source_env['localhost_container'].get('container_ref', None) is None:
                container_manager = self.source_env['localhost_container']['container_manager']

                container_config = self.source_env['localhost_container']['container_config']
                container_config['name'] = self.source_name

                self.source_env['localhost_container']['container_ref'] = container_manager.get_or_start(container_config)


            container = self.source_env['localhost_container']['container_ref']
            status = container.state.status
            if status == 'running':
                return True
            else:
                return False


        return False



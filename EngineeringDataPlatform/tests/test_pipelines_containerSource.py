
import EngineeringDataPlatform as edp
from EngineeringDataPlatform.pipeline.source.source_mongodb import Source_MongoDB
from EngineeringDataPlatform.pipeline.container import WorkspaceContainerManager

from python_on_whales import docker

def test_startMongodb():
    pass





workspace = edp.workspace.create_workspace_if_not_existing("workspace_test")
containerManager = WorkspaceContainerManager(workspace)


source_env = {'source_env': 'localhost_container',
              'localhost_container': {'container_manager': containerManager,
                                      'connection_url': 'mongodb://localhost',
                                      'container_config': {'image': 'mongo',
                                                           'ports': [27017]}}}

mongo_source = Source_MongoDB('mongo_test', source_env, workspace, read_only=False)

if mongo_source.is_source_available():
    mongo_source.connect()

print()

mongo_source.write({'database_name': 'mydatabase',
                    'collection': 'mycollection',
                    'data': { "name": "John",
                              "address": "Highway 37" }})

results = mongo_source.read({'database_name': 'mydatabase',
                          'collection': 'mycollection'})

#docker.ps(all=True)
#my_container = docker.run("ubuntu", detach=True, name='ubuntu_edp_myworkspace2')

# mongo = docker.run("mongo", publish=[(27017, 27017)], detach=True, name='mongodb_edp_myworkspace')
#
#
# import pymongo
# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["mydatabase"]
# mycol = mydb["customers"]
#
# mydict = { "name": "John", "address": "Highway 37" }
#
# x = mycol.insert_one(mydict)


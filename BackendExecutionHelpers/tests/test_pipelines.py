

from BackendExecutionHelpers.BEH.ETL.ETL_Manager import ETLManager
from BackendExecutionHelpers.BEH.Workspaces.DataManager import DataManager
from BackendExecutionHelpers.BEH.Pipelines.Pipeline_Manager import PipelineManager
from BackendExecutionHelpers.BEH.Pipelines.Pipeline import Pipeline
from BackendExecutionHelpers.BEH.Pipelines.Pipeline_Item import PipelineItem
from BackendExecutionHelpers.BEH.Pipelines.Pipeline_Source_DataManager import PipelineSource_DataManager
from BackendExecutionHelpers.BEH.Pipelines.Pipeline_Transform_Python import Pipeline_Transform_Python
from BackendExecutionHelpers.BEH.Pipelines.Pipeline_Source_SQLite import Pipeline_Source_SQLite

def test_pipelinesource_datamanager():
    __dataManager = DataManager()
    __etlManager = ETLManager(__dataManager)

    # load some data in
    config = {"filepath": "E:/Projects/DataPlatform/TestData/mhnc.us.txt",
              "etl_type": "LoadSingle_Local"}

    __etlManager.New_ETL_FromConfig(config)
    __etlManager.ComputeCycle()

    # create a pipeline source item from this loaded dataset
    itemConfig = {'pipeline_item_unique_name': 'raw_stock_data',
                  'pipeline_item_type': 'DataManagerSource',
                  'pipeline_item_type_config': {'DataManagerName': 'mhnc_us_txt'}}


    newSource = PipelineSource_DataManager(itemConfig, __dataManager)
    newSource.execute()

    # and lets just make sure it's available as an output to (not yet defined) dependencies
    assert newSource.has_output()
    assert newSource.get_output().shape[0] > 100 # we have some data at least


def test_pipelinetransform_python():
    # lets now do a two item pipeline with a source and a pipeline
    # basically the same setup as just the source verification, but now lets do something with it
    __dataManager = DataManager()
    __etlManager = ETLManager(__dataManager)

    # load some data in
    config = {"filepath": "E:/Projects/DataPlatform/TestData/mhnc.us.txt",
              "etl_type": "LoadSingle_Local"}

    __etlManager.New_ETL_FromConfig(config)
    __etlManager.ComputeCycle()

    newPipeline = Pipeline()

    # create a pipeline source item from this loaded dataset
    sourceConfig = {'pipeline_item_unique_name': 'raw_stock_data',
                  'pipeline_item_type': 'DataManagerSource',
                  'pipeline_item_type_config': {'DataManagerName': 'mhnc_us_txt'}}


    newSource = PipelineSource_DataManager(sourceConfig, __dataManager)
    newPipeline.add_item(newSource)
    newSource.execute()



    transformCode = "return raw_stock_data['Open']*2"
    transformConfig = {'pipeline_item_unique_name': 'test_transform',
                      'pipeline_item_type': 'PythonTransform',
                      'pipeline_item_type_config': {'input_item_names': ['raw_stock_data'],
                                                    'language': 'python',
                                                    'env': 'default',
                                                    'code': transformCode}}

    newTransform = Pipeline_Transform_Python(transformConfig, __dataManager)
    newPipeline.add_item(newTransform)
    newTransform.execute()

    assert newTransform.has_output()
    expectedOutput = newSource.output['Open'] * 2
    assert newTransform.output.equals(expectedOutput)


def test_sqlite_readwrite():
    # and now lets see if we can write to a SQLite database
    __dataManager = DataManager()
    __etlManager = ETLManager(__dataManager)

    # load some data in
    config = {"filepath": "E:/Projects/DataPlatform/TestData/mhnc.us.txt",
              "etl_type": "LoadSingle_Local"}

    __etlManager.New_ETL_FromConfig(config)
    __etlManager.ComputeCycle()

    newPipeline = Pipeline()

    # create a pipeline source item from this loaded dataset
    sourceConfig = {'pipeline_item_unique_name': 'raw_stock_data',
                  'pipeline_item_type': 'DataManagerSource',
                  'pipeline_item_type_config': {'DataManagerName': 'mhnc_us_txt'}}


    newSource = PipelineSource_DataManager(sourceConfig, __dataManager)
    newPipeline.add_item(newSource)
    newSource.execute()



    transformConfigWriteSQL = {'pipeline_item_unique_name': 'test_sqlite_write',
                      'pipeline_item_type': 'WriteToSQLite',
                      'pipeline_item_type_config': {'input_item_names': ['raw_stock_data'],
                                                    'output_table_names': {'raw_stock_data': 'test_sqlite_stock_data'},
                                                    'db': {'type': 'sqlite',
                                                           'address': 'pythonsqlite_tests.db'}
                                                    }}

    newDBWrite = Pipeline_Source_SQLite(transformConfigWriteSQL, __dataManager)
    newPipeline.add_item(newDBWrite)
    newDBWrite.execute()

    assert newDBWrite.has_output()
    assert 'db' in newDBWrite.output and 'table_names' in newDBWrite.output


    transformConfigReadSQL = {'pipeline_item_unique_name': 'test_sqlite_read',
                              'pipeline_item_type': 'ReadFromSQLite',
                              'pipeline_item_type_config': {'table': 'test_sqlite_stock_data',
                                                            'db': {'type': 'sqlite',
                                                                   'address': 'pythonsqlite_tests.db'}
                                                            }}

    newDBRead = Pipeline_Source_SQLite(transformConfigReadSQL, __dataManager)
    newPipeline.add_item(newDBRead)
    newDBRead.execute()

    assert newDBRead.has_output()
    assert newSource.output.equals(newDBRead.output)




import BackendExecutionHelpers.BEH.Workspaces.DataManager
from BackendExecutionHelpers.BEH.ETL.ETL_CSV import ETL_CSV
from BackendExecutionHelpers.BEH.ETL.ETL_Manager import ETLManager
from BackendExecutionHelpers.BEH.Workspaces.DataManager import DataManager



def test_LoadSingle_Local_defaultParams():
    __dataManager = DataManager()
    __etlManager = ETLManager(__dataManager)

    config = {"filepath": "E:/Projects/DataPlatform/TestData/mhnc.us.txt",
              "etl_type": "LoadSingle_Local"}

    __etlManager.New_ETL_FromConfig(config)
    __etlManager.ComputeCycle()

    assert 'default_namespace' in __dataManager._data
    assert 'mhnc_us_txt' in __dataManager._data['default_namespace']


def test_LoadFolder_Local_defaultParams():
    __dataManager = DataManager()
    __etlManager = ETLManager(__dataManager)

    config = {"directory": "E:/Projects/DataPlatform/TestData/intraday_combined_tickers",
              "etl_type": "LoadFolder_Local"}

    __etlManager.New_ETL_FromConfig(config)
    __etlManager.ComputeCycle()

    assert 'default_namespace' in __dataManager._data
    assert len(__dataManager._data['default_namespace']) == 3 # we have them all and nothing else
    assert 'NYSE_20190102_60_txt' in __dataManager._data['default_namespace']
    assert 'NYSE_20190103_60_txt' in __dataManager._data['default_namespace']
    assert 'NYSE_20190104_60_txt' in __dataManager._data['default_namespace']


def test_LoadSingle_Local_CustomTransform():
    __dataManager = DataManager()
    __etlManager = ETLManager(__dataManager)

    config = {"filepath": "E:/Projects/DataPlatform/TestData/mhnc.us.txt",
     "etl_type": "LoadSingle_Local",
     "custom_transform_function": "def CustomTransform12345(etl_params):\n    path = etl_params['filepath']\n    lines = []\n    with open(path, 'r') as f:\n        for line in f:\n            lines.append(line.split(','))\n    return lines",
              "custom_transform_function_name": "CustomTransform12345"}

    __etlManager.New_ETL_FromConfig(config)
    __etlManager.ComputeCycle()

    assert 'default_namespace' in __dataManager._data
    assert 'mhnc_us_txt' in __dataManager._data['default_namespace']


def test_LoadFolder_Local_CustomTransform():
    __dataManager = DataManager()
    __etlManager = ETLManager(__dataManager)

    config = {"directory": "E:/Projects/DataPlatform/TestData/intraday_combined_tickers",
              "etl_type": "LoadFolder_Local",
              "custom_transform_function": "def CustomTransform123456(etl_params, path):\n    lines = []\n    with open(path, 'r') as f:\n        for line in f:\n            lines.append(line.split(','))\n    return lines",
              "custom_transform_function_name": "CustomTransform123456"}

    __etlManager.New_ETL_FromConfig(config)
    __etlManager.ComputeCycle()

test_LoadFolder_Local_CustomTransform()
test_LoadSingle_Local_CustomTransform()
test_LoadSingle_Local_defaultParams()
test_LoadFolder_Local_defaultParams()


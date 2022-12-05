
import EngineeringDataPlatform as edp
from EngineeringDataPlatform.pipeline import Pipeline, PipelineItem
from EngineeringDataPlatform.pipeline import transforms



def test_examples():
    workspace = edp.workspace.create_workspace_if_not_existing("workspace_test")

    a = PipelineItem(edp.pipeline.extracts.extract_example, {'name': 'extract_example', 'inputs': None})
    b = PipelineItem(transforms.transform_example, {'name': 'transform_example', 'inputs': ['extract_example'], 'multiplyBy': 3})
    c = PipelineItem(edp.pipeline.loads.load_example, {'name': 'load_example', 'inputs': ['transform_example']})

    p = Pipeline([a, b, c], workspace).execute()

    assert p.steps_list[1].results is not None


def test_loadCSV():
    workspace = edp.workspace.create_workspace_if_not_existing("workspace_test")

    a = PipelineItem(edp.pipeline.extracts.read_csv, {'name': 'test_readCsv',
                                                      'inputs': None,
                                                      'path': "E:/Projects/DataPlatform/TestData/intraday_combined_tickers/NYSE_20190102_60.txt"})
    p = Pipeline([a], workspace)
    p.execute()

    assert p.steps_list[0].results is not None
    assert p.steps_list[0].results.shape[0] > 1000


def test_replaceColumnNames():
    workspace = edp.workspace.create_workspace_if_not_existing("workspace_test")

    a = PipelineItem(edp.pipeline.extracts.read_csv, {'name': 'test_readCsv',
                                                      'inputs': None,
                                                      'path': "E:/Projects/DataPlatform/TestData/intraday_combined_tickers/NYSE_20190102_60.txt"})
    b = PipelineItem(transforms.column_names_replace, {'name': 'test_colReplace',
                                                                    'inputs': 'test_readCsv',
                                                                    'values': ['ticker', 'date','open','high','low','close','vol']})
    p = Pipeline([a, b], workspace)
    p.execute()

    assert p.steps_list[1].results.columns.values[0] == 'ticker'


def test_funcModifyColumnNames():
    workspace = edp.workspace.create_workspace_if_not_existing("workspace_test")

    a = PipelineItem(edp.pipeline.extracts.read_csv, {'name': 'test_readCsv',
                                                      'inputs': None,
                                                      'path': "E:/Projects/DataPlatform/TestData/intraday_combined_tickers/NYSE_20190102_60.txt"})

    def colNameModify(strVal):
        return strVal.replace('<', '').replace('>', '').strip().upper()

    b = PipelineItem(transforms.column_names_funcmodify, {'name': 'test_colFuncMod',
                                                                    'inputs': 'test_readCsv',
                                                                    'func': colNameModify})
    p = Pipeline([a, b], workspace)
    p.execute()

    assert p.steps_list[1].results.columns.values[0] == 'TICKER'


def test_splitByCategoricalColVal():

    workspace = edp.workspace.create_workspace_if_not_existing("workspace_test")

    a = PipelineItem(edp.pipeline.extracts.read_csv, {'name': 'test_readCsv',
                                                      'inputs': None,
                                                      'path': "E:/Projects/DataPlatform/TestData/intraday_combined_tickers/NYSE_20190102_60.txt"})

    def colNameModify(strVal):
        return strVal.replace('<', '').replace('>', '').strip().upper()

    b = PipelineItem(transforms.column_names_funcmodify, {'name': 'test_colFuncMod',
                                                                    'inputs': 'test_readCsv',
                                                                    'func': colNameModify})

    c = PipelineItem(transforms.split_by_categorical_col_value, {'name': 'tickerSplit',
                                                                              'inputs': 'test_colFuncMod',
                                                                              'col': 'TICKER'})

    # def tickerFilter(df):
    #     return df.loc[0, 'TICKER'][0] in ['A','B','C']
    #
    # d = PipelineItem(dep.pipeline.transforms.filter_list_by_func, {'name': 'tickerFilter',
    #                                                                'inputs': 'tickerSplit',
    #                                                                'func': tickerFilter})

    d = PipelineItem(transforms.take_sample_from_list, {'name': 'tickerSample',
                                                                     'inputs': 'tickerSplit',
                                                                     'sample_method': 'random',
                                                                     'sample_num': 5,
                                                                     'random_seed': 0})

    def tableName(df):
        return df.loc[0, 'TICKER']

    e = PipelineItem(transforms.commit_to_workspace_db, {'name': 'commitSample',
                                                                      'inputs': 'tickerSample',
                                                                      'table_name_method': 'func',
                                                                      'func': tableName})

    p = Pipeline([a, b, c, d, e], workspace)
    p.execute()

    assert p.steps_list[1].results.columns.values[0] == 'TICKER'
    assert len(p.steps_indexed['tickerSplit'].results) > 100

test_splitByCategoricalColVal()
test_funcModifyColumnNames()
test_replaceColumnNames()
test_loadCSV()
test_examples()



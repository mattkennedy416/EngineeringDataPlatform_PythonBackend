

from EngineeringDataPlatform.workspace.Workspace import Workspace

import psycopg2
from sqlalchemy import create_engine

from EngineeringDataPlatform.workspace.WorkspaceHelpers import exists

def _createNewPostgresDatabase(name):
    # establishing the connection
    conn = psycopg2.connect(
        database="postgres", user='postgres', password='dafgag416', host='127.0.0.1', port='5432'
    )
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Preparing query to create a database
    #sql = '''CREATE database mydb''';
    sql = "CREATE database " + name

    # Creating a database
    cursor.execute(sql)
    print("Database created successfully........")

    # Closing the connection
    conn.close()


def _checkIfPostgresDatabaseExists(name):
    conn = psycopg2.connect(
        database="postgres", user='postgres', password='dafgag416', host='127.0.0.1', port='5432'
    )
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Preparing query to create a database
    #sql = '''CREATE database mydb''';
    sql = "select exists( SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower('" + name + "') );"

    # Creating a database
    cursor.execute(sql)
    dbExists = cursor.fetchall()[0][0]

    # Closing the connection
    conn.close()

    return dbExists


def _deleteWorkspace(name):
    """
    Delete the workspace passed in from disk
    :param workspace:
    :return:
    """


    conn = psycopg2.connect(
        database="postgres", user='postgres', password='dafgag416', host='127.0.0.1', port='5432'
    )
    conn.autocommit = True

    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    sql = 'DROP DATABASE IF EXISTS ' + name + ';'

    cursor.execute(sql)

    # Closing the connection
    conn.close()


def create_workspace_if_not_existing(name):
    """
    What do we need to do here?
    - figure out where we're going on disk
    - check if workspace already exists
    - check if database already exists in postgres
    - create new postgres database
    - setup project structure
        - data
        - pipelines
        - analysis
    :param name:
    :return:
    """
    dbname = name
    if _checkIfPostgresDatabaseExists(name):
        # load the workspace details and initialize it
        pass
    else:
        _createNewPostgresDatabase(dbname)

    engine = create_engine('postgresql://postgres:dafgag416@localhost:5432/'+dbname)
    return Workspace(name, engine, dbname)








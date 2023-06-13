# import sqlalchemy as DB
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
import sqlite3
from sqlite3 import Error, OperationalError
from _utilities_ import flatten_list
import pandas as pd
import numpy as np


def SELECT(database, tableName, query):
    List = []
    sqliteConnection = None
    sqliteConnection = sqlite3.connect(database)
    cursor = sqliteConnection.cursor()
    rows = cursor.execute(query)
    for row in rows:
        List.append(row)

    # --Get Column Names
    desc = rows.description
    List1 = list(desc)
    colNames = []
    for x in range(len(List1)):
        p = [t for t in List1[x] if t != None][0]
        colNames.append(p)

    df = pd.DataFrame(List)
    df.columns = tuple(colNames)

    cursor.close()
    sqliteConnection.close()

    return df


def SELECT_ALL(database, tableName):
    List = []
    sqliteConnection = None
    sqliteConnection = sqlite3.connect(database)
    cursor = sqliteConnection.cursor()
    rows = cursor.execute(f"SELECT * FROM {tableName}")
    for row in rows:
        List.append(row)

    # --Get Column Names
    desc = rows.description
    List1 = list(desc)
    colNames = []
    for x in range(len(List1)):
        p = [t for t in List1[x] if t != None][0]
        colNames.append(p)

    df = pd.DataFrame(List)
    df.columns = tuple(colNames)

    cursor.close()
    sqliteConnection.close()

    return df


def DROP(database, tableName):
    sqliteConnection = None
    sqliteConnection = sqlite3.connect(database)
    cursor = sqliteConnection.cursor()
    cursor.execute(f"DROP TABLE {tableName}")
    sqliteConnection.commit()
    cursor.close()
    sqliteConnection.close()


def UPDATE(database, TABLE, id, sqlColumn, value):
    sqliteConnection = None
    sqliteConnection = sqlite3.connect(database)
    cursor = sqliteConnection.cursor()
    cursor.execute(f'update {TABLE} set {sqlColumn} = {value} where id = "{id}"')
    sqliteConnection.commit()
    cursor.close()
    sqliteConnection.close()


def TABLE_EXISTS(TABLE=None, database=None):
    if TABLE is None:
        pass
    else:
        ##--Get List of Tables
        try:
            # Making a connection between sqlite3
            # database and Python Program
            sqliteConnection = None
            sqliteConnection = sqlite3.connect(database)

            # If sqlite3 makes a connection with python
            # program then it will print "Connected to SQLite"
            # Otherwise it will show errors
            # print("Connected to SQLite")

            # Getting all tables from sqlite_master
            sql_query = """SELECT name FROM sqlite_master
    	WHERE type='table';"""

            # Creating cursor object using connection object
            cursor = sqliteConnection.cursor()

            # executing our sql query
            cursor.execute(sql_query)

            # printing all tables list
            check = cursor.fetchall()

            if (
                len(
                    [tbl for tbl in flatten_list(check) if TABLE in flatten_list(check)]
                )
                == 0
            ):
                return False
            else:
                return True

        except sqlite3.Error as error:
            print("Failed to execute the above query", error)

        finally:

            # Inside Finally Block, If connection is
            # open, we need to close it
            if sqliteConnection:

                # using close() method, we will close
                # the connection
                cursor.close()
                sqliteConnection.close()
                del sqliteConnection

                # After closing connection object, we
                # will print "the sqlite connection is
                # closed"
                # print("the sqlite connection is closed")




def INSERT(database, sqlTable, sqlColumns, values):
    # from _CloudAuth_ import save_database
    try:
        sqliteConnection = None
        sqliteConnection = sqlite3.connect(database)
        print("Connected to SQLite")
        cursor = sqliteConnection.cursor()
        INSERT_INTO = f'INSERT INTO {sqlTable} ({", ".join(sqlColumns)}) VALUES ({", ".join(["?"[:5]] * len(values.iloc[0]))})'
        cursor.executemany(INSERT_INTO, values.values)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        pError = str(error)
        print("Failed to insert multiple records into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def INSERT_NOT_IN(database, sqlTableIN, sqlTableFROM, sqlColumns, lookupColumn):
    # from _CloudAuth_ import save_database
    try:
        sqliteConnection = None
        sqliteConnection = sqlite3.connect(database)
        print("Connected to SQLite")
        cursor = sqliteConnection.cursor()
        INSERT_INTO = f"""INSERT INTO {sqlTableIN} ({", ".join(sqlColumns)})
                  SELECT * FROM {sqlTableFROM} WHERE {lookupColumn} IN (SELECT {lookupColumn} FROM {sqlTableFROM} WHERE {lookupColumn} NOT IN (SELECT {lookupColumn} FROM {sqlTableIN}));
                  """
        cursor.execute(INSERT_INTO)
        sqliteConnection.commit()
        cursor.close()
    except sqlite3.Error as error:
        pError = str(error)
        print("Failed to insert multiple records into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")


def SELECT_QUERY(database, query):
    try:
        List = []
        sqliteConnection = None
        sqliteConnection = sqlite3.connect(database)
        print("Connected to SQLite")
        cursor = sqliteConnection.cursor()
        rows = cursor.execute(query)
        for row in rows:
            List.append(row)
        # --Get Column Names
        desc = rows.description
        List1 = list(desc)
        colNames = []
        for x in range(len(List1)):
            p = [t for t in List1[x] if t != None][0]
            colNames.append(p)
        df = pd.DataFrame(List)
        if df.empty == False:
            df.columns = tuple(colNames)
            cursor.close()
            return df
        else:
            return df
    except sqlite3.Error as error:
        pError = str(error)
        print("Query Failed", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

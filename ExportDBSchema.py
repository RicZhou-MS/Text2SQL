# import streamlit as st
import pyodbc
from GlobalClasses import *

# Get the environment variables
GlobalContext()


def init_connection():
    return pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};SERVER="
        + GlobalContext.DB_SERVER
        + ";DATABASE="
        + GlobalContext.DB_NAME
        + ";UID="
        + GlobalContext.DB_USER
        + ";PWD="
        + GlobalContext.DB_USER_PASS
    )


conn = init_connection()


def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()


def get_tables():
    return run_query("SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")


def get_columns(schema_name, table_name):
    return run_query(f"select COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, NUMERIC_PRECISION, DATETIME_PRECISION, IS_NULLABLE from INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{schema_name}' AND TABLE_NAME = '{table_name}'")


with open('.\DBSchema.txt', 'w') as f:
    # Print results and write to file.
    for tb_row in get_tables():
        print(f"[{tb_row[0]}].[{tb_row[1]}]")
        f.write(f"\n[{tb_row[0]}].[{tb_row[1]}] \n")
        for col_row in get_columns(tb_row[0], tb_row[1]):
            column_name = col_row[0]
            data_type = col_row[1]
            character_maximum_length = col_row[2]
            if character_maximum_length is not None and character_maximum_length > 0:
                data_type = f"{data_type}({character_maximum_length})"
            print(f"-{column_name}")
            f.write(f"-{column_name}  \n")

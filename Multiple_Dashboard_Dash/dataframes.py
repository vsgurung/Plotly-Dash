"""
Description: This files creates the dataframe which can be imported by other apps
"""
import cx_Oracle
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime

# def get_database_connection(username, password, host, port, sid):
#     with cx_Oracle.connect(f'{username}/{password}@{host}:{port}/{sid}') as cnxn:
#         if cnxn:
#             return cnxn
#         else:
#             error = 'Problem with connection'
#             return error
#
# db_cnxn = get_database_connection(username, password, host, port , sid)
#
# def get_dataframe(db_connection):
#     dataframe = pd.read_sql('SELECT * FROM GAPMINDER', con=db_connection)
#     return dataframe
#
# df = get_dataframe(db_cnxn)

engine = create_engine('oracle+cx_oracle://username:password@localhost/xe')

mpg_df = pd.read_sql("""SELECT * FROM MPG""", con=engine)
gapminder_df = pd.read_sql("""SELECT * FROM GAPMINDER""", con=engine)
iris_df = pd.read_sql("""SELECT * FROM IRIS_DATASET""",con=engine)

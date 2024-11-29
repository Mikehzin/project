import pyodbc
import os

DEBUG = True
threaded = True

conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};' \
           'SERVER=192.168.100.199;' \
           'DATABASE=GS_DATA;' \
           'UID=sa;' \
           'PWD=ruqaBAvU7?g6!T'

conn = pyodbc.connect(conn_str)

SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc:///?odbc_connect={}'.format(conn_str)

SECRET_KEY = 'GalanteS2'

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/imagem'


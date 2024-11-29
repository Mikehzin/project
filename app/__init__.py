from flask import Flask
import urllib
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_socketio import SocketIO, emit
import pyodbc
from flask_login import LoginManager, current_user
from flask_cors import CORS

app = Flask(__name__)

app.config.from_object('config')
manager = Manager(app)

conn_str = 'DRIVER={ODBC Driver 17 for SQL Server};' \
           'SERVER=192.168.100.199;' \
           'DATABASE=GS_DATA;' \
           'UID=sa;' \
           'PWD=ruqaBAvU7?g6!T'

conn = pyodbc.connect(conn_str)

app.config["SQLALCHEMY_DATABASE_URI"] = 'mssql+pyodbc:///?odbc_connect={}'.format(conn_str)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)


manager.add_command('db', MigrateCommand)

from app.models import tables
from app.controllers import default
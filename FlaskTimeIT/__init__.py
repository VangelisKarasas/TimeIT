from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import pyodbc


app = Flask(__name__)
app.config['SECRET_KEY'] = '17d5414078e4aee783a8e7579a5ed52e'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@LAPTOP-DENNTC5N\\MSSQLSERVER03/TimeManagement?driver=ODBC+Driver+17+for+SQL+Server'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from FlaskTimeIT import routes  # noqa: E402,F401

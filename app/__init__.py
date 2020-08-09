from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../fyt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Guptaji the great'

db = SQLAlchemy(app)
login_manager=LoginManager(app)
migrate = Migrate(app,db)

from . import routes
from . import models


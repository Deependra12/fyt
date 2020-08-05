from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  flask_login import LoginManager

app = Flask(__name__)
login_manager=LoginManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fyt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Guptaji the great'

db = SQLAlchemy(app)

from . import routes
from . import models

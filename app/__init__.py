from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../fyt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Guptaji the great'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USERNAME']='fytnepal@gmail.com'
app.config['MAIL_PASSWORD']='kuproject22'


db = SQLAlchemy(app)
login_manager=LoginManager(app)
migrate = Migrate(app,db)
mail = Mail(app)


from . import routes
from . import models


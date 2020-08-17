from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../fyt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SENDER'] = 'FYT Admin <{0}>'.format(app.config['MAIL_USERNAME'])

app.config["RECAPTCHA_PUBLIC_KEY"] = "6Le-EsAZAAAAAAQ24AEYft1b3RQ9BruHwJ9nfE7m "
app.config["RECAPTCHA_PRIVATE_KEY"] = "6Le-EsAZAAAAALcaQUSPzGJs-BxURauFIfai__lo"


db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app,db,render_as_batch= True)
mail = Mail(app)
ser=URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))



from . import routes
from . import models


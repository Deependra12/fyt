from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
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
app.config['GOOGLE_MAP_API_KEY'] = os.environ.get('GOOGLE_MAP_API_KEY')
app.config['OPENCAGE_GEOCODE_API_KEY'] = os.environ.get("OPENCAGE_GEOCODE_API_KEY")

# set optional bootswatch theme

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = u"You need to login to access that page!"
login_manager.login_message_category = "danger"

migrate = Migrate(app, db, render_as_batch=True)
mail = Mail(app)
ser = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))

from . import routes
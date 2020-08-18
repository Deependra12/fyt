from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
import flask_monitoringdashboard as dashboard


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

# set optional bootswatch theme

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

#captcha

app.config["RECAPTCHA_PUBLIC_KEY"] = os.environ.get('PUBLIC_KEY')
app.config["RECAPTCHA_PRIVATE_KEY"] = os.environ.get('PRIVATE_KEY')
#dashboard
#useful for admin
dashboard.config.init_from(file='config.cfg')

dashboard.bind(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app,db,render_as_batch= True)
mail = Mail(app)
ser = URLSafeTimedSerializer(os.environ.get('SECRET_KEY'))
admin = Admin(app, name='Find Your Tutor', template_mode='bootstrap3')

#Add base_template='admin/admin.html' in Admin to use manually defined template.

from . import routes
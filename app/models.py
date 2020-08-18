from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from . import ModelView, admin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    hash_password = db.Column(db.String(120))
    role = db.Column(db.String(7), index=True)
    student = db.relationship('Student', backref='base', uselist=False)
    teacher = db.relationship('Tutor', backref='base', uselist=False)

    def __repr__(self):
        return '<Email {}>'.format(self.email)

    def set_password(self, password):
        self.hash_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password, password)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    phone = db.Column(db.Integer)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))

class Tutor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    phone = db.Column(db.Integer)
    user_id = db.Column(db.Integer , db.ForeignKey('user.id'))

class UserView(ModelView):
    form_columns = ['username', 'email', 'role']

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

# For general models, admin.add_view(ModelView(User, db.session)) 
admin.add_view(UserView(User, db.session))
from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(120))
    phone = db.Column(db.Integer, index=True, unique=True)

    def __repr__(self):
        return '<Email {}>'.format(self.email)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Tutor(User, db.Model):
    pass


class Student(User, db.Model):
    pass


@login_manager.user_loader
def load_tutor(email):
    return Tutor.query.get(email)

@login_manager.user_loader
def load_student(email):
    return Student.query.get(email)

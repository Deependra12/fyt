import os.path as op

from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from flask_admin.menu import MenuLink
from flask_admin.contrib.fileadmin import FileAdmin

from . import db, login_manager
from . import  app, Admin, ModelView, AdminIndexView


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    hash_password = db.Column(db.String(120))
    role = db.Column(db.String(7), index=True)
    student = db.relationship('Student', backref='base', uselist=False, cascade="all, delete")
    teacher = db.relationship('Tutor', backref='base', uselist=False, cascade="all, delete")
    location = db.relationship('Location', backref='User', uselist=False, cascade="all, delete")
    mycourse = db.relationship('Mycourse', backref='User', cascade="all, delete")
    
    def __repr__(self):
        return '<Email {}>'.format(self.email)

    def set_password(self, password):
        self.hash_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hash_password, password)

    def set_location(self):
        self.location = Location(User=self)

    def update_location(self, **kwargs):
        for column,value in kwargs.items():
            location = self.location
            setattr(location,column,value)
        db.session.commit()

    def set_tutor(self):
        self.teacher = Tutor(base=self)

    def update_tutor(self, **kwargs):
        for column,value in kwargs.items():
            tutor = self.teacher
            setattr(tutor,column,value)
        db.session.commit()

    def set_student(self):
        self.student = Student(base=self)
    
    def update_student(self, **kwargs):
        for column,value in kwargs.items():
            student = self.student
            setattr(student,column,value)
        db.session.commit()

class Student(db.Model):
    phone = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True,)
    full_name = db.Column(db.String(64))
    guardian_name = db.Column(db.String(64))
    guardian_address = db.Column(db.String(64))
    guardian_phone = db.Column(db.Integer)
    state = db.Column(db.String(64))
    district = db.Column(db.String(64))
    municipality = db.Column(db.String(64))
    ward_no = db.Column(db.Integer)
    date_of_birth = db.Column(db.String(64))
    profile_pic = db.Column(db.String(255))
    description = db.Column(db.String(1000))

    def __repr__(self):
        student = User.query.filter_by(id = self.user_id ).first()
        return '<Email {}>'.format(student.email)


class Tutor(db.Model):
    phone = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True,)
    full_name = db.Column(db.String(64))
    state = db.Column(db.String(64))
    district = db.Column(db.String(64))
    municipality = db.Column(db.String(64))
    ward_no = db.Column(db.Integer)
    date_of_birth = db.Column(db.String(64))
    profile_pic = db.Column(db.String(255))
    description = db.Column(db.String(1000))
    experience = db.relationship('Experience', backref='Tutor', uselist=True ,cascade="all, delete")
    qualification = db.relationship('Qualification', backref='Tutor', uselist=True ,cascade="all, delete")
    achievement = db.relationship('Achievement', backref='Tutor', uselist=True ,cascade="all, delete")

    def __repr__(self):
        tutor = User.query.filter_by(id = self.user_id ).first()
        return '<Email {}>'.format(tutor.email)


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.user_id'))
    experience = db.Column(db.String(255))
    experience_file = db.Column(db.String(255))


class Qualification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.user_id'))
    qualification = db.Column(db.String(255))
    qualification_file = db.Column(db.String(255))


class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_id = db.Column(db.Integer, db.ForeignKey('tutor.user_id'))
    achievement = db.Column(db.String(255))
    achievement_file = db.Column(db.String(255))


class Location(db.Model):
    travel_distance = db.Column(db.String(64))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    place_details = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_title = db.Column(db.String(100), nullable=False)
    course_level = db.Column(db.String(100), nullable=False)
    course_description = db.Column(db.String(1000))
    mycourse = db.relationship('Mycourse', backref='Course', cascade="all, delete")
    

class Mycourse(db.Model):
    id = db.Column(db.Integer, primary_key=True)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    time = db.Column(db.Time)
    cost = db.Column(db.String(64))


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# Admin Panel


class AdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        abort(401)


admin = Admin(app, name='FYT Admin', template_mode='bootstrap3', index_view=AdminView())


class CustomView(ModelView):
    can_create = False
    can_edit = False

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        abort(401)


class UserView(CustomView):
    column_exclude_list = ['hash_password',] 
    column_searchable_list = ['username', 'email']
    column_filters = ['role']


class CourseView(ModelView):
    form_choices = {
        'course_level': [
            ('basic','Basic Education(Grade 1-8)'),
            ('secondary','Secondary Education(Grade 9-12)'),
            ('bachelor','Bachelor Level'),
            ('master','Master Level')
        ]
    }
    form_create_rules = ('course_title', 'course_level', 'course_description')
    form_edit_rules = ('course_title', 'course_level', 'course_description')




class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated    


# For general models, admin.add_view(ModelView(User, db.session)) 
admin.add_view(UserView(User, db.session))
admin.add_view(CustomView(Student, db.session))
admin.add_view(CustomView(Tutor, db.session))
admin.add_view(CustomView(Location, db.session)) 
admin.add_view(CourseView(Course, db.session))
admin.add_view(CustomView(Experience, db.session))
admin.add_view(CustomView(Achievement, db.session))
admin.add_view(CustomView(Qualification, db.session))

path = op.join(op.dirname(__file__), 'static/docs/')
admin.add_view(FileAdmin(path, '/static/docs/', name='Documents'))

admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))
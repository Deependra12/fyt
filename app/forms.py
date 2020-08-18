from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import Student, Tutor


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = IntegerField('Phone', validators=[DataRequired()])
    role = SelectField('Role', choices=[('teacher','Teacher'),('student','Student')], validators=[DataRequired()] )
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        tutor = Tutor.query.filter_by(username=username.data)
        student = Student.query.filter_by(username=username.data)
        user = student.union_all(tutor).first()
        if user:
            raise ValidationError('That username is taken. Please choose a new username.')

    def validate_email(self, email):
        tutor = Tutor.query.filter_by(email=email.data)
        student = Student.query.filter_by(email=email.data)
        user = student.union_all(tutor).first()
        if user:
            raise ValidationError('That email is taken. Please choose a new email.')

    def validate_phone(self, phone):
        tutor = Tutor.query.filter_by(phone=phone.data)
        student = Student.query.filter_by(phone=phone.data)
        user = student.union_all(tutor).first()
        if user:
            raise ValidationError('That phone is taken. Please choose a new phone.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('continue')


class ResetLinkForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Email')
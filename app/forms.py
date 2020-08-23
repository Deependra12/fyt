from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, IntegerField, SubmitField, SelectField, Label
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import User
import json

# Activate captcha later on using
# {{form.recaptcha()}} 

class RegistrationForm(FlaskForm):
    # recaptcha = RecaptchaField()
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = IntegerField('Phone', validators=[DataRequired()])
    role = SelectField('Role', choices=[('teacher', 'Teacher'), ('student', 'Student')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a new username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a new email.')


class LoginForm(FlaskForm):
    # recaptcha = RecaptchaField()
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('continue')


class ResetLinkForm(FlaskForm):
    # recaptcha = RecaptchaField()
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Email')



class MyLocationForm(FlaskForm):
    latitude = StringField('Latitude', validators=[DataRequired()], render_kw={'readonly':True})
    longitude = StringField('Longitude', validators=[DataRequired()], render_kw={'readonly':True})
    place = StringField('Place Details', validators=[DataRequired()], render_kw={'readonly':True})
    travel_distance = SelectField('Distance Willing To Travel (in kms)', validators=[DataRequired()])
    # state = SelectField(label="State", validators=[DataRequired()])
    # district = SelectField(label='District', validators=[DataRequired()])
    # municipality = StringField('Municipality', validators=[DataRequired()])
    # wardno = StringField('Ward Number', validators=[DataRequired()])
    geolocation_misguide_info = Label("geolocation-misguide-info","Location here is shown using your device location, which probably may be misguided. Please click your actual location below.")
    submit = SubmitField('Save')
    update = SubmitField('Edit')

    def create_choices_from_list(self,lists):
        choices = []
        for L in lists:
            choices.append((L, L))
        return choices

    def create_travel_distance_choice(self):
        distances = ['O km (home)']
        for d in range(5, 55, 5):
            distances.append(str(d - 5) + '-' + str(d) + ' km')
        distance_choice = self.create_choices_from_list(distances)
        self.travel_distance.choices = distance_choice



    


    

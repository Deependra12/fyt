from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField, PasswordField, IntegerField, SubmitField, SelectField, DateField,
                    FileField, Label, TimeField, MultipleFileField, TextAreaField)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from flask_wtf.file import FileRequired, FileAllowed
from .models import User


def create_choices_from_list(lists):
    choices = []
    for L in lists:
        choices.append((L, L))
    return choices


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=6, message='Password length should be at least 6')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = StringField('Phone', validators=[DataRequired(),Length(max=10,min=7, message="Phone number can't exceed 10 digits")])
    role = SelectField('Role', choices=[('tutor', 'Tutor'), ('student', 'Student')], validators=[DataRequired()])
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
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(),Length(min=6, message='Password length should be at least 6')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Change Password')


class ResetLinkForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Email')


class MyLocationForm(FlaskForm):
    latitude = StringField('Latitude', validators=[DataRequired()], render_kw={'readonly':True})
    longitude = StringField('Longitude', validators=[DataRequired()], render_kw={'readonly':True})
    place = StringField('Place Details', validators=[DataRequired()], render_kw={'readonly':True})
    geolocation_misguide_info = Label("geolocation-misguide-info","Location here is shown using your device location, which probably may be misleading. Please mark your actual location below.")
    submit = SubmitField('Save')
    update = SubmitField('Edit')

   
class PersonalInfoForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    date_of_birth = StringField('Date of Birth', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    state = SelectField(label="State", validators=[DataRequired()])
    district = SelectField(label='District', validators=[DataRequired()])
    municipality = StringField('Municipality', validators=[DataRequired()])
    ward_no = StringField('Ward Number', validators=[DataRequired()])
    self_description = TextAreaField ("Describe yourself!", validators=[Length(max=250)])
    profile_pic = FileField('Profile Picture', validators=[FileAllowed(['jpeg','jpg'], 'Images Only!')])    
    submit = SubmitField('Save')
    
    def create_state_choices(self):
        states = ['Province 1', 'Province 2', 'Bagmati', 'Gandaki', 'Province 5', 'Karnali', 'Sudurpaschim']
        state_choice = create_choices_from_list(states)
        self.state.choices = state_choice

    def create_district_choices(self):
        D = ['Bhojpur', 'Dhankuta', 'Ilam', 'Jhapa', 'Khotang', 'Morang', 'Okhaldhunga', 
            'Panchthar', 'Sankhuwasabha', 'Solukhumbu', 'Sunsari', 'Taplejung', 'Terhathum', 'Udayapur',
            'Saptari', 'Siraha', 'Dhanusa', 'Mahottari', 'Sarlahi', 'Bara', 'Parsa', 'Rautahat',
            'Sindhuli', 'Ramechhap', 'Dolakha', 'Bhaktapur', 'Dhading', 'Kathmandu', 'Kavrepalanchok', 
            'Lalitpur', 'Nuwakot', 'Rasuwa', 'Sindhupalchok', 'Chitwan', 'Makwanpur',
            'Baglung', 'Gorkha', 'Kaski', 'Lamjung', 'Manang', 'Mustang', 'Myagdi', 'Nawalpur', 
            'Parbat', 'Syangja', 'Tanahun', 'Kapilvastu', 'Parasi', 'Rupandehi', 'Arghakhanchi', 
            'Gulmi', 'Palpa', 'Dang', 'Pyuthan', 'Rolpa', 'Rukum ( Eastern )', 'Banke', 'Bardiya', 
            'Rukum ( Western )', 'Salyan', 'Dolpa', 'Humla', 'Jumla', 'Kalikot', 'Mugu', 'Surkhet', 'Dailekh','Jajarkot', 
            'Kailali', 'Achham', 'Doti', 'Bajhang', 'Bajura', 'Kanchanpur', 'Dadeldhura', 'Baitadi', 'Darchula']
        districts = sorted(D)
        district_choice = create_choices_from_list(districts)
        self.district.choices = district_choice


class StudentPersonalInfoForm(PersonalInfoForm):
    guardian_name = StringField("Guardian's Full Name", validators=[DataRequired()])
    guardian_address = StringField("Guardian's Address", validators=[DataRequired()])
    guardian_phone = StringField("Guardian's Phone Number", validators=[DataRequired()])


class AccountInfoForm(FlaskForm):
    old_password = PasswordField('Give Your Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(),Length(min=6, message='Password length should be at least 6')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update')


class MyCourseForm(FlaskForm):
    education_level = StringField("Education Level", validators=[DataRequired()])
    course = StringField("Course", validators=[DataRequired()])
    cost = SelectField('Monthly Cost', validators=[DataRequired()])
    starttime = TimeField('Start Time', validators=[DataRequired()])
    endtime = TimeField('End Time', validators=[DataRequired()])
    save = SubmitField('Save')
    
    def create_cost_choices(self):
        cost = []
        for d in range(1000, 10000, 1000):
            cost.append((d,'Rs. ' + str(d)))
        self.cost.choices = cost


class MyExperienceForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    institution = StringField("Institution", validators=[DataRequired()])
    experience = StringField("Experience", validators=[DataRequired()])
    experience_certificate = FileField("Certification for your experience", validators=[FileRequired(), FileAllowed(['pdf','docx','doc','png','jpeg','jpg'], 'File format must be .pdf, .docx, .doc, .png, .jpeg or .jpg!')])
    save_experience = SubmitField("Save")


class MyQualificationForm(FlaskForm):
    qualification = StringField("Qualification", validators=[DataRequired()])
    institution = StringField ("Institution", [DataRequired()])
    qualification_date = DateField("Qualification Date", [DataRequired()])
    qualification_certificate = FileField("Certification for your qualification", validators=[FileRequired(), FileAllowed(['pdf','docx','doc','png','jpeg','jpg'], 'File format must be .pdf, .docx, .doc, .png, .jpeg or .jpg!')])
    save_qualification = SubmitField("Save")


class MyAchievementForm(FlaskForm):
    achievement = StringField ("Achievement", [DataRequired()])
    awarded_by = StringField("Awarded By",[DataRequired()])
    awarded_date = DateField("Awarded Date", [DataRequired()])
    achievement_certificate = FileField("Certification for your achievement", validators=[FileRequired(), FileAllowed(['pdf','docx','doc','png','jpeg','jpg'], 'File format must be .pdf, .docx, .doc, .png, .jpeg or .jpg!')])
    save_achievement = SubmitField("Save")
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import (StringField, PasswordField, IntegerField, SubmitField, SelectField, DateField,
                    FileField, Label, TimeField, MultipleFileField, TextAreaField)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import User

# Activate captcha later on using
# {{form.recaptcha()}} 

def create_choices_from_list(lists):
    choices = []
    for L in lists:
        choices.append((L.lower().replace(' ',''), L))
    return choices

class RegistrationForm(FlaskForm):
    # recaptcha = RecaptchaField()
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone = IntegerField('Phone', validators=[DataRequired()])
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
    geolocation_misguide_info = Label("geolocation-misguide-info","Location here is shown using your device location, which probably may be misguided. Please click your actual location below.")
    submit = SubmitField('Save')
    update = SubmitField('Edit')

    def create_travel_distance_choice(self):
        distances = ['O km (home)']
        for d in range(5, 55, 5):
            distances.append(str(d - 5) + '-' + str(d) + ' km')
        distance_choice = create_choices_from_list(distances)
        self.travel_distance.choices = distance_choice


class PersonalInfoForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    date_of_birth = StringField('Date of Birth', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    state = SelectField(label="State", validators=[DataRequired()])
    district= SelectField(label='District', validators=[DataRequired()])
    municipality = StringField('Municipality', validators=[DataRequired()])
    ward_no = StringField('Ward Number', validators=[DataRequired()])
    self_description = TextAreaField ("Describe yourself!")
    profile_pic = FileField('Profile Picture')    
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
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update')


class MyCourseForm(FlaskForm):
    education_level = SelectField("Education Level", validators=[DataRequired()])
    course = SelectField("Course", validators=[DataRequired()])
    cost = SelectField('Cost', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    add = SubmitField("Add New Course")
    save = SubmitField('Save')
    
    def create_cost_choices(self):
        cost = []
        for d in range(500, 5500, 500):
            cost.append('Rs. ' + str(d - 500) + ' - ' + 'Rs. ' + str(d))
        cost_choice = create_choices_from_list(cost)
        self.cost.choices = cost_choice

class MyExperienceForm(FlaskForm):
    experience = StringField (label="Experience", validators=[DataRequired()])
    experience_certificate = FileField("Certification for your experience", [DataRequired()])
    save_experience = SubmitField("Save")

class MyQualificationForm(FlaskForm):
    qualification = StringField ("Qualification", [DataRequired()])
    qualification_certificate = FileField("Certification for your qualification", [DataRequired()])
    save_qualification = SubmitField("Save")

class MyAchievementForm(FlaskForm):
    achievement = StringField ("Achievement", [DataRequired()])
    achievement_certificate = FileField("Certification for your achievement", [DataRequired()])
    save_achievement = SubmitField("Save")

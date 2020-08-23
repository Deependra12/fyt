from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from .models import User


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
    # distances_choice = create_choices_from_list(distances)
    travel_distance = SelectField('Distance Willing To Travel (in kms)', validators=[DataRequired()], choices=[('a','a')])
    state = SelectField(label="State", validators=[DataRequired()])
    district = SelectField(label='District', validators=[DataRequired()])
    municipality = StringField('Municipality', validators=[DataRequired()])
    wardno = StringField('Ward Number', validators=[DataRequired()])

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

    def create_state_choice(self):
        states=['Province 1', 'Province 2', 'Bagmati', 'Gandaki', 'Province 5', 'Karnali', 'Sudurpaschim']
        state_choice = self.create_choices_from_list(states)
        self.state.choices = state_choice

    def create_district_choice(self):
        districts=["Bhojpur", "Dhankuta", "Ilam", "Jhapa", "Khotang", "Morang", "Okhaldhunga",
            "Panchthar", "Sankhuwasabha", "Solukhumbu", "Sunsari", "Taplejung",
            "Terhathum", "Udayapur", "Saptari", "Siraha", "Dhanusa", "Mahottari",
            "Sarlahi", "Bara", "Parsa", "Rautahat", "Sindhuli", "Ramechhap", "Dolakha",
            "Bhaktapur", "Dhading", "Kathmandu", "Kavrepalanchok", "Lalitpur", "Nuwakot",
            "Rasuwa", "Sindhupalchok", "Chitwan", "Makwanpur", "Baglung", "Gorkha", "Kaski",
            "Lamjung", "Manang", "Mustang", "Myagdi", "Nawalpur", "Parbat", "Syangja", "Tanahun",
            "Kapilvastu", "Parasi", "Rupandehi", "Arghakhanchi", "Gulmi", "Palpa", "Dang",
            "Pyuthan", "Rolpa", "Rukum ( Eastern )", "Banke", "Bardiya", "Rukum ( Western )", "Salyan",
            "Dolpa", "Humla", "Jumla", "Kalikot", "Mugu", "Surkhet", "Dailekh", "Jajarkot", "Kailali",
            "Achham", "Doti", "Bajhang", "Bajura", "Kanchanpur", "Dadeldhura", "Baitadi", "Darchula"
        ]
        districts.sort()
        district_choice = self.create_choices_from_list(districts)
        self.district.choices = district_choice



    


    

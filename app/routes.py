from flask import (
    render_template, 
    redirect, 
    url_for, 
    jsonify, 
    request, 
    flash,
    session,
    abort,
)

from flask_login import (
    login_required,
    login_user,
    logout_user,
    current_user,
)

from . import app, db
from . import login_manager
from . import email as em
from .forms import (
    RegistrationForm, 
    LoginForm, 
    ResetForm, 
    ResetLinkForm, 
    MyLocationForm, 
    PersonalInfoForm,
    StudentPersonalInfoForm,
    AccountInfoForm,
    MyCourseForm,
)
from .models import User, Student, Tutor
from .admin import admin

def redirect_user(user):
    if user.role == 'student':
        return redirect(url_for('student'))
    elif user.role == 'tutor':
        return redirect(url_for('tutor'))
    else:
        return redirect('/admin')

def is_tutor(user):
    if user.role == 'tutor':
        return True
    elif user.role == 'student':
        return False
    elif user.role == 'admin':
        return False

@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route('/home')
def home():
    if current_user.is_authenticated:
        return redirect_user(current_user)
    return render_template('index.html')

@app.route('/a/login', methods=['GET', 'POST'])
def admin_login():
    """ Carry out admin login """
    if current_user.is_authenticated:
        return redirect_user(current_user)
    form = LoginForm()
    if form.validate_on_submit():
        if not admin.check_password(form.password.data):
            flash('Invalid admin login', 'danger')
            return redirect(url_for('admin_login'))
        login_user(admin)
        flash('Successfully logged in.', 'success')
        return redirect('/admin')
    return render_template('login.html', form=form, admin=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Carry out user login """
    if current_user.is_authenticated:
        return redirect_user(current_user)
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect (url_for('login'))
        login_user(user)
        flash('Successfully logged in.', 'success')
        return redirect_user(current_user)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def user_register():
    """ Carry out user registration """
    if current_user.is_authenticated:
        return redirect_user(current_user)
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        if is_tutor(user):
            tutor = Tutor(phone=form.phone.data, base=user)
            db.session.add(tutor)
        else:
            student = Student(phone=form.phone.data, base=user)
        db.session.commit()
        #message = "Welcome to Find Your Tutor"
        #em.send_mail(username, role, message, email)
        flash('Your account was created.\nYou can now Login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/password-reset', methods=['GET', 'POST'])
def passwordresetlink():
    form = ResetLinkForm()
    email = form.email.data
    if form.validate_on_submit():
        em.send_reset_mail(email)
        return redirect(url_for('login'))
    return render_template('resetlink.html', form=form)

@app.route('/reset', methods=['GET', 'POST'])
def passwordreset():
    form = ResetForm()
    unhashed_password = form.password.data
    return render_template('reset.html', form=form)

@app.route('/hello/<token>')
def hello(token):
    try:
        email = ser.loads(token, salt='email-confirm', max_age=36)
    except :
        return '<h1>The token has expired!<h1>'
    return '<h1>The token is valid!<h1>'

@app.route("/logout")
def logout():
    """ Log users out of their accounts """
    logout_user()
    flash('You are now logged out. Log in to continue!', 'success')
    return redirect(url_for('login'))

@app.route('/about-us')
def about_us():
    """ Render the about us page """
    return render_template('about.html')

#@app.route('/student/<username>')
#@login_required
#def student(username):
#    user = User.query.filter_by(username=username).first()
#    if user.username == current_user.username and user.role == 'student':
#        return render_template("student.html", user=user, 
#           profilepic=url_for('static',filename='images/student.jpeg'))
#    else:
#        return render_template("404.html")

@app.route('/student/home')
@login_required
def student():
    """ Render the student account page """
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect('/admin')
    user = User.query.filter_by(username=current_user.username).first()
    if user.username == current_user.username and user.role == 'student':
        return render_template('student.html', user=user, profilepic=url_for('static', 
            filename='images/student.jpeg'))
    abort(404)

#@app.route('/tutor/<username>')
#@login_required
#def tutor(username):
#    user = User.query.filter_by(username=username).first()
#    if user.username == current_user.username and user.role == 'teacher':
#        return render_template("tutor.html", user=user, profilepic=url_for('static',
#           filename='images/teacher.jpg'))
#    else:
#        return render_template("404.html")

@app.route('/tutor/home')
@login_required
def tutor():
    """ Render the tutor account page """
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect('/admin')
    user = User.query.filter_by(username=current_user.username).first()
    if user.username == current_user.username and is_tutor(user):
        return render_template("tutor.html", user=user, profilepic=url_for('static',
            filename='images/teacher.jpg'))
    abort(404)

#@login_manager.user_loader
#def load_user(login_id):
#    user_ = get_user(login_id)
#    if user_:
#        return User(login_id, user_['role'])
#    else:
#       user_ = get_admin(login_id)
#       if user_:
#            return User(login_id, 'a')

def fetch_optional_view(role, option):
    """ Get the view of pages accourding to the context """
    google_api = ''
    opencage_api = ''
    if option == 'mylocation':
        form = MyLocationForm()
        form.create_travel_distance_choice()
        google_api = app.config.get('GOOGLE_MAP_API_KEY')
        opencage_api = app.config.get('OPENCAGE_GEOCODE_API_KEY')
    elif option == "personal-info":
        if is_tutor(current_user):
            form = PersonalInfoForm()
        else:
            form = StudentPersonalInfoForm()
            form.create_state_choices()
    elif option == "account-info":
        form = AccountInfoForm()
    elif option == "my-courses":
        form = MyCourseForm()
        form.create_cost_choices()
    else:
        form = None
    user = User.query.filter_by(username=current_user.username).first()
    if user.username == current_user.username and not is_tutor(user):
        return render_template(option+".html", user=user, profilepic=url_for('static', 
            filename='images/student.jpeg'), form=form, google_api_key=google_api, 
            opencage_api_key=opencage_api)
    elif user.username == current_user.username and is_tutor(user):
        return render_template(option+".html", user=user, profilepic=url_for('static',
            filename='images/teacher.jpg'), form=form, google_api_key=google_api, 
            opencage_api_key=opencage_api)

@app.route('/<role>/<option>')
@login_required
def user_option(role, option):
    """ Handle redirection of user related routes """
    view = fetch_optional_view(role, option)
    if view:
        return view
    abort(404)

@app.errorhandler(404)
def content_not_found_handler(e):
    """ For Handling 404 error """
    return render_template('404.html')

@app.errorhandler(401)
def unauthorized_access_handler(e):
    """ For Handling 401 error """
    flash('You must be logged in to access this page!', 'danger')
    return redirect(url_for('login'))
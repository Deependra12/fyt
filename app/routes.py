from flask import (
    render_template, 
    redirect, 
    url_for, 
    jsonify, 
    request, 
    flash,
    session
)
from flask_login import (
    login_required,
    login_user,
    logout_user
)

from . import app, db
from .forms import RegistrationForm, LoginForm
from . import  login_manager
from .user import User
from .mockusers import (get_user, add_user)

@app.route('/')
@app.route('/index')
def index():
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/a/login', methods=['GET', 'POST'])
def admin_login():
    ''' Route for admin login '''
    if request.method == "POST":
        # replace with WTF forms later on
        login_id = request.form.get('login-id', '')
        login_password = request.form.get('login-password', '')
        print(login_id, login_password)
        return redirect(url_for('admin_login'))
    return render_template('admin-login.html')


@app.route('/login',methods=['GET', 'POST'] )
def login():
    ''' Route for tutor/student login '''
    form = LoginForm()
    if form.validate_on_submit():
        #getting email and password from forms.py
        email=form.email.data
        password=form.password.data
        #getting stored user from mockuser.py
        stored_user=get_user(email)
        #Checking if given email is in stored user or not
        #Also checking if password is correct or not
        if stored_user and stored_user['password']==password:
            #Flashing message to announce successful login
            flash('Login successful','success')
            #making object of User class from user.py
            user=User(email)
            #adding user to login_user method of flask_login module
            login_user(user,remember=True)
            #checking role of logging user
            if stored_user['role']=='student':
                return redirect(url_for('student'))
            else:
                return redirect(url_for('tutor'))
        else:
            flash('Please check your email or password','danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    #getting data from form.py
    form = RegistrationForm()
    email=form.email.data
    password=form.password.data
    role=form.role.data
    print(role)
    phone=form.phone.data
    #validating the filled up information
    if form.validate_on_submit():
        #checking if same email is already registered
        if get_user(email):
            return render_template('register.html', form=form)
        #Announcing succssful registration
        flash('Your account was created, You can now Login !', 'success')
        #Add new user to mockuser in mockuser.py
        add_user(email,password,role,phone)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect((url_for("home")))

@app.route('/about-us')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def error_handler(e):
    ''' For Handling 404 error '''
    return render_template('404.html')

@app.route('/student')
@login_required
def student():
    return render_template("student.html")

@app.route('/tutor')
@login_required
def tutor():
    return render_template("tutor.html")

@login_manager.user_loader
def load_user(email):
    user_password=get_user(email)
    if user_password:
        return User(email)
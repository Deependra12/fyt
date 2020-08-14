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
    logout_user,
    current_user
)

from . import app, db
from .forms import RegistrationForm, LoginForm
from . import  login_manager
from .user import User
from .mockusers import get_admin, get_user, add_user
from .passwordhash import PasswordHasher
from . import email as em

PH = PasswordHasher()


@app.route('/')
@app.route('/index')
def index():
    if(current_user.is_authenticated):
        print("ram")
        return redirect(url_for('login'))
    return redirect(url_for('home'))


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/a', methods=['GET', 'POST'])
def admin_login():
    ''' Route for admin login '''
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        stored_admin = get_admin(username)
        if stored_admin and PH.validate_password(password,stored_admin['salt'],
                stored_admin['password']):
            user = User(username,role='a')
            login_user(user, remember=True)
            return redirect(url_for("admin"))
    return render_template('admin/admin-login.html')


@app.route('/admin')
def admin():
    return render_template("admin/admin.html")


@app.route('/login', methods=['GET', 'POST'] )
def login():
    ''' Route for tutor/student login '''
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            #getting email and password from forms.py
            email  = form.email.data
            password = form.password.data
            #getting stored user from mockuser.py
            stored_user = get_user(email)
            #Checking if given email is in stored user or not
            #Also checking if password is correct or not
            if stored_user and PH.validate_password(password, stored_user['salt'], 
                    stored_user['password']):
                #Flashing message to announce successful login
                flash('Login successful', 'success')
                #making object of User class from user.py
                role = stored_user['role']
                print(f"The role is: {role}")
                user = User(email, role)
                #adding user to login_user method of flask_login module
                login_user(user, remember=True)
                #checking role of logging user
                if stored_user['role'] == 'student':
                    return redirect(url_for('student'))
                else:
                    return redirect(url_for('tutor'))
            else:
                flash('Please check your email or password','danger')
        return render_template('login.html', form=form)
    else:
        role = current_user.get_role()
        print(role)
        if role == 'student':
            return redirect(url_for('student'))
        else:
            return redirect(url_for('tutor'))


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    #getting data from form.py
    form = RegistrationForm()
    username = form.username.data
    email = form.email.data
    role = form.role.data
    phone = form.phone.data
    unhashed_password = form.password.data
    #validating the filled up information
    if form.validate_on_submit():
        #checking if same email is already registered
        if get_user(email):
            return render_template('register.html', form=form)
        #Announcing succssful registration
        flash('Your account was created, You can now Login !', 'success')
        #Add new user to mockuser in mockuser.py
        # Salting and hashing provided password
        salt = PH.salting()
        hashed_password = PH.hash(salt + unhashed_password)
        add_user(username, email, role, phone, salt, hashed_password)
        message="Welcome to Find Your Tutor"
        em.send_mail(message,email)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/about-us')
def about():
    return render_template('about.html')


@app.route('/student')
@login_required
def student():
    return render_template("student.html")


@app.route('/tutor')
@login_required
def tutor():
    return render_template("tutor.html")


@login_manager.user_loader
def load_user(login_id):
    user_ = get_user(login_id)
    if user_:
        return User(login_id, user_['role'])
    else:
        user_ = get_admin(login_id)
        if user_:
            return User(login_id, 'a')


@app.errorhandler(404)
def error_handler(e):
    ''' For Handling 404 error '''
    return render_template('404.html')
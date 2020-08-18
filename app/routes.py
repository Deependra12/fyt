from flask import (
    render_template, 
    redirect, 
    url_for, 
    jsonify, 
    request, 
    flash,
    session,
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
from .forms import RegistrationForm, LoginForm, ResetForm, ResetLinkForm
#from .user import User
#from .mockusers import get_admin, get_user, add_user
#from .passwordhash import PasswordHasher
from .models import Tutor, Student


def redirect_user(manche):
    if Tutor.query.filter_by(email=manche.email).first():
        return redirect(url_for('tutor'))
    elif Student.query.filter_by(email=manche.email).first():
        return redirect(url_for('student'))


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
    return redirect(url_for('home'))


@app.route('/home')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('login'))
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
            user = User(username, role='a')
            login_user(user, remember=True)
            return redirect(url_for("admin"))
    return render_template('admin/admin-login.html')


@app.route('/admin')
def admin():
    return render_template("admin/admin.html")


@app.route('/login', methods=['GET', 'POST'] )
def login():
    if current_user.is_authenticated:
        return redirect_user(current_user)
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data)
        tutor = Tutor.query.filter_by(email=form.email.data)
        user = student.union_all(tutor).first()
        if not user or not user.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect (url_for('login'))
        login_user(user)
        flash('Successfully logged in.','success')
        return redirect_user(current_user)
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    if current_user.is_authenticated:
        return redirect_user(current_user)
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.role.data == "teacher":
            user = Tutor(username=form.username.data, email=form.email.data, phone=form.phone.data)
        else:
            user = Student(username=form.username.data, email=form.email.data, phone=form.phone.data)
        user.set_password(form.password.data)
        db.session.add(user)
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
    logout_user()
    return redirect(url_for("home"))


@app.route('/about-us')
def about_us():
    return render_template('about.html')


#@app.route('/student/<username>')
#@login_required
#def student(username):
#    user = User.query.filter_by(username=username).first()
#    if user.username == current_user.username and user.role == 'student':
#        return render_template("student.html", user=user, profilepic=url_for('static',filename='images/student.jpeg'))
#    else:
#        return render_template("404.html")

@app.route('/student/home')
@login_required
def student():
    user = Student.query.filter_by(username=current_user.username).first()
    if user:
        return render_template("student.html", user=user, profilepic=url_for('static', 
            filename='images/student.jpeg'))
    else:
        return render_template("404.html")


#@app.route('/tutor/<username>')
#@login_required
#def tutor(username):
#    user = User.query.filter_by(username=username).first()
#    if user.username == current_user.username and user.role == 'teacher':
#        return render_template("tutor.html", user=user, profilepic=url_for('static',filename='images/teacher.jpg'))
#    else:
#        return render_template("404.html")

@app.route('/tutor/home')
@login_required
def tutor():
    user = Tutor.query.filter_by(username=current_user.username).first()
    if user:
        return render_template("tutor.html", user=user, profilepic=url_for('static',filename='images/teacher.jpg'))
    else:
        return render_template("404.html")

#@login_manager.user_loader
#def load_user(login_id):
#    user_ = get_user(login_id)
#    if user_:
#        return User(login_id, user_['role'])
#    else:
#       user_ = get_admin(login_id)
#       if user_:
#            return User(login_id, 'a')


@app.errorhandler(404)
def error_handler(e):
    ''' For Handling 404 error '''
    return render_template('404.html')

@app.errorhandler(401)
def error_handler(e):
    ''' For Handling 401 error '''
    flash('You must be logged in to access this page!', 'danger')
    return redirect(url_for('login'))
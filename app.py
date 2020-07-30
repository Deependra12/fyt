from flask import (
    Flask,
    render_template, 
    redirect, 
    url_for, 
    jsonify, 
    request, 
    flash,
    session
)
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fyt.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Guptaji the great'

db = SQLAlchemy(app)


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
        if form.email.data == 'check@gmail.com' and form.password.data == 'guptaji':
            session.user = form.email.data
            print (session.user)
            flash('Login successful','success')
            return redirect(url_for('home'))
        else:
            flash('Please check your email or password','danger')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def user_register():
    ''' Route for user registration '''
    form = RegistrationForm() 
    if form.validate_on_submit():
        flash('Your account was created, You can now Login !', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/about-us')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def error_handler(e):
    ''' For Handling 404 error '''
    return render_template('404.html')


if __name__=='__main__':
    app.run(debug=True)
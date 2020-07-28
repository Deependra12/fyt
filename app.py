from flask import Flask, render_template, redirect, url_for, jsonify, request 

app = Flask(__name__)

@app.route('/')
@app.route('/home')
@app.route('/index')
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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/tutors/login')
def tutor_home():
    return "Tutors login"

@app.route('/students')
def students_home():
    return "Students login"

@app.errorhandler(404)
def error_handler(e):
    ''' For Handling 404 error '''
    #replace this with a page for 404 error
    return "<h1>Sorry, URL not found!</h1>"


if __name__=='__main__':
    app.run(debug=True)
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/home')
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/tutors')
def teachers():
    return "Tutors"

@app.route('/students')
def students():
    return "Students"

if __name__=='__main__':
    app.run(debug=True)
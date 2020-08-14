from flask_mail import Message
from . import app,mail
from .routes import render_template

def send_mail(username,role,message, email):
    msg = Message(message,
                  sender=app.config.get('MAIL_USERNAME','fytnepal@gmail.com'),
                  recipients=[email])
    msg.body="welcome you have been registered\n"
    msg.html=render_template('email.html', username=username,role=role,sending_mail=True)

   
    mail.send(msg)

    

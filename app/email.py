from flask_mail import Message
from . import app,mail

def send_mail(message, email):
    msg = Message(message,
                  sender=app.config.get('MAIL_USERNAME','fytnepal@gmail.com'),
                  recipients=[email])
    msg.body="welcome you have been registered\n"
    mail.send(msg)

    

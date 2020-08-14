from flask import render_template
from flask_mail import Message

from . import app,mail


def send_mail(username, role, message, email):
    print(app.config.get('MAIL_USERNAME'))
    msg = Message(
            message,
            sender=app.config.get('MAIL_USERNAME'),
            recipients=[email]
        )
    msg.body = "Welcome you have been registered!\n"
    msg.html = render_template('email.html', username=username, role=role, sending_mail=True)

    mail.send(msg)
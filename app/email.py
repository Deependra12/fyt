from flask import render_template, url_for
from flask_mail import Message

from . import app, mail, ser


def send_mail(username, role, message, email):
    msg = Message(
            message,
            sender=app.config.get('MAIL_SENDER'),
            recipients=[email]
        )
    msg.html = render_template('email-templates/registration-mail.html', username=username, role=role,
                                sending_mail=True, email=app.config.get('MAIL_USERNAME'))
    mail.send(msg)

def send_reset_mail(email):
    msg = Message(
            'Password Reset Link',
            sender=app.config.get('MAIL_SENDER'),
            recipients=[email]
        )
    token = ser.dumps(email, salt='email-confirm')
    link = url_for('hello', token=token, external=True)
    msg.html = render_template('email-templates/pwd-reset-mail.html', link=link, sending_mail=True)
    mail.send(msg)
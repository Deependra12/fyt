from flask import render_template, url_for
from flask_mail import Message

from . import app,mail


def send_mail(username, role, message, email):
    # print(app.config.get('MAIL_USERNAME'))
    msg = Message(
            message,
            sender=app.config.get('MAIL_SENDER'),
            recipients=[email]
        )
    msg.html = render_template('email.html', username=username, role=role, sending_mail=True,
                               email=app.config.get('MAIL_USERNAME'))

    mail.send(msg)
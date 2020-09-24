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

def send_reset_mail(user):
    token=user.get_reset_token(expires_sec=1800)
    msg = Message(
            '[Find Your Tutor] Password Reset Link',
            sender=app.config.get('MAIL_SENDER'),
            recipients=[user.email]
        )
    msg.html = render_template('email-templates/pwd-reset-mail.html', user=user, token=token)
    mail.send(msg)


def send_announcements_mail(title, message, email_list):
    msg = Message(
            f'[Find Your Tutor] {title}',
            sender=app.config.get('MAIL_SENDER'),
            recipients=[*email_list]
        )
    msg.body = message
    mail.send(msg)
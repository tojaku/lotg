import random
import string
import hashlib
from flask.ext.mail import Message
from flask.ext.babel import gettext as _
from flask import render_template, url_for
from config import DEFAULT_MAIL_SENDER, SITE_NAME


def random_string(length):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(length)])


def password_hash(password):
    digest = hashlib.md5(password)
    return digest.hexdigest()


def message_confirmation(uid, email, cstring):
    msg = Message(_('Account confirmation'), sender=DEFAULT_MAIL_SENDER, recipients=[email])
    msg.html = render_template('email/confirmation.html',
                               site_name=SITE_NAME,
                               user=email,
                               confirmation_link=url_for('confirm', uid=uid, cstring=cstring, _external=True))
    return msg


def message_reset_password(email, password):
    msg = Message(_('Reset password'), sender=DEFAULT_MAIL_SENDER, recipients=[email])
    msg.html = render_template('email/reset_password.html',
                               site_name=SITE_NAME,
                               user=email,
                               password=password)
    return msg
import random
import string
import hashlib
from flask.ext.mail import Message
from flask.ext.babel import gettext as _, format_datetime
from flask import render_template, url_for, g
from config import DEFAULT_MAIL_SENDER, SITE_NAME
from functools import wraps


def random_string(length):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(length)])


def password_hash(password):
    digest = hashlib.md5(password)
    return digest.hexdigest()


def access_allowed(target_level, exclusive=False):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_level = 0
            if g.user is not None:
                user_level = g.user.security_level

            allowed = False
            if exclusive is True and user_level == target_level or exclusive is False and user_level >= target_level:
                allowed = True
            if not allowed:
                return render_template('access_denied.html')

            return f(*args, **kwargs)

        return wrapped

    return wrapper


def jinja_format_datetime(value, dt_format='dd. MMMM yyyy HH:mm'):
    return format_datetime(value, dt_format)


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
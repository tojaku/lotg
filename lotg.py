import hashlib
import datetime
import random
import string

from flask import Flask, render_template, g, request, flash, url_for, redirect, session
from flask.ext.babel import Babel, gettext as _
from flask.ext.mail import Mail, Message
from sqlalchemy.exc import IntegrityError

from config import LANGUAGES, DEFAULT_MAIL_SENDER, SITE_NAME
from models import db, User
from forms import SignInForm, SignUpForm

app = Flask(__name__)
app.config.from_object('config')

mail = Mail(app)
babel = Babel(app)
db.init_app(app)


@app.before_request
def before_request():
    if 'user_id' in session:
        user_id = session['user_id']
        g.user = User.query.get_or_404(user_id)
    else:
        g.user = None


@babel.localeselector
def get_locale():
    if g.user is not None:
        return g.user.language
    return request.accept_languages.best_match(LANGUAGES.keys())


@babel.timezoneselector
def get_timezone():
    if g.user is not None:
        return g.user.timezone
    return None


# ROUTES


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sign_up', methods=('GET', 'POST'))
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User()
        user.email = form.email.data
        digest = hashlib.md5(form.password.data)
        user.password = digest.hexdigest()
        user.signed_up = datetime.datetime.utcnow()
        user.language = form.language.data
        user.timezone = form.timezone.data
        user.confirmation_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(20)])
        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError as err:
            if err.message.find(user.email) != -1:
                form.email.errors.append(_('E-mail address is in use'))
        else:
            msg = Message(_('Account confirmation'), sender=DEFAULT_MAIL_SENDER, recipients=[user.email])
            msg.html = render_template('email/confirmation.html',
                                       site_name=SITE_NAME,
                                       user=user.email,
                                       confirmation_link=url_for('confirm',
                                                                 id=user.id,
                                                                 key=user.confirmation_string,
                                                                 _external=True))
            mail.send(msg)
            flash(_('Successful sign up, check your e-mail'))
            return redirect('')

    return render_template('sign_up.html', form=form)


@app.route('/sign_in', methods=('GET', 'POST'))
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        digest = hashlib.md5(form.password.data)
        password_hash = digest.hexdigest()
        user = User.query.filter_by(email=form.email.data, password=password_hash).first()
        if user is None:
            flash(_('Wrong email or password'))
        elif user.active is False:
            flash(_('Your account is deactivated'))
        elif user.confirmed is False:
            flash(_('Your account is not confirmed'))
        else:
            session['user_id'] = user.id
            flash(_('Successfully signed in') + ' ' + user.email)
            return redirect('')

    return render_template('sign_in.html', form=form)


@app.route('/sign_out')
def sign_out():
    session.clear();
    flash(_('Successfully signed out'))
    return redirect('')


@app.route('/confirm/<uid>/<key>')
def confirm(uid, key):
    user = User.query.filter_by(id=uid, confirmation_string=key).first_or_404()
    if user is None:
        flash(_('Wrong confirmation data'))
    else:
        user.confirmed = True
        db.session.commit()
        flash(_('Confirmation success'))
    return redirect('')


if __name__ == '__main__':
    app.run()

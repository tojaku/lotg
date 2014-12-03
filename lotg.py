import hashlib
import datetime
import random
import string

from flask import Flask, render_template, g, request, flash
from flask.ext.babel import Babel, gettext as _
from flask.ext.mail import Mail, Message

from config import LANGUAGES, DEFAULT_MAIL_SENDER
from models import db, User
from forms import SignInForm, SignUpForm

app = Flask(__name__)
app.config.from_object('config')

mail = Mail(app)
babel = Babel(app)
db.init_app(app)


@app.before_request
def before_request():
    g.user = None
    '''if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?', [session['user_id']], one=True)'''


@babel.localeselector
def get_locale():
    if g.user is not None:
        return g.user.locale
    return request.accept_languages.best_match(LANGUAGES.keys())


@babel.timezoneselector
def get_timezone():
    if g.user is not None:
        return g.user.timezone


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/sign_in', methods=('GET', 'POST'))
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        return 'Success'
    return render_template('sign_in.html', form=form)


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
        db.session.commit()

        flash(_('Successful sign up, check your e-mail'))

        msg = Message('Hello', sender=DEFAULT_MAIL_SENDER, recipients=[user.email])
        msg.body = user.confirmation_string
        mail.send(msg)
    return render_template('sign_up.html', form=form)


if __name__ == '__main__':
    app.run()

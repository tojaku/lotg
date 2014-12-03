import hashlib
import datetime
import random
import string

from flask import Flask, render_template, g, request, flash, url_for, redirect
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
            msg = Message('Hello', sender=DEFAULT_MAIL_SENDER, recipients=[user.email])
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
        return 'Success'
    return render_template('sign_in.html', form=form)


@app.route('/confirm/<id>/<key>', methods=('GET', 'POST'))
def confirm(id, key):
    return 'OK';


if __name__ == '__main__':
    app.run()

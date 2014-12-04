import datetime
from flask import Flask, render_template, g, request, flash, redirect, session
from flask.ext.babel import Babel, gettext as _, format_datetime
from flask.ext.mail import Mail
from sqlalchemy.exc import IntegrityError
from config import LANGUAGES
from models import db, User
from forms import SignInForm, SignUpForm, AccountProblemForm
from helpers import random_string, message_confirmation, message_reset_password, password_hash

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


@app.template_filter('datetime')
def tpl_format_datetime(value, dt_format='dd. MMMM yyyy HH:mm'):
    return format_datetime(value, dt_format)


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
        user.password = password_hash(form.password.data)
        user.signed_up = datetime.datetime.utcnow()
        user.language = form.language.data
        user.timezone = form.timezone.data
        user.confirmation_string = random_string(20)
        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError as err:
            if err.message.find(user.email) != -1:
                form.email.errors.append(_('E-mail address is in use'))
        else:
            msg = message_confirmation(user.id, user.email, user.confirmation_string)
            mail.send(msg)
            flash(_('Successful sign up, check your e-mail'))
            return redirect('')

    return render_template('sign_up.html', form=form)


@app.route('/sign_in', methods=('GET', 'POST'))
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, password=password_hash(form.password.data)).first()
        if user is None:
            flash(_('Wrong email or password'))
        elif user.active is False:
            flash(_('Your account is deactivated'))
        elif user.confirmed is False:
            flash(_('Your account is not confirmed'))
        else:
            session['user_id'] = user.id
            user.signed_in = datetime.datetime.utcnow()
            db.session.commit()
            flash(_('Successfully signed in') + ' ' + user.email)
            return redirect('')

    return render_template('sign_in.html', form=form)


@app.route('/sign_out')
def sign_out():
    session.clear()
    flash(_('Successfully signed out'))
    return redirect('')


@app.route('/confirm/<uid>/<cstring>')
def confirm(uid, cstring):
    user = User.query.filter_by(id=uid, confirmation_string=cstring).first_or_404()
    if user is None:
        flash(_('Wrong confirmation data'))
    else:
        user.confirmed = True
        db.session.commit()
        flash(_('Confirmation success'))

    return redirect('')


@app.route('/account_problem', methods=('GET', 'POST'))
def account_problem():
    form = AccountProblemForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            form.email.errors.append(_('Unknown e-mail address'))
        elif form.problem.data == 'confirmation':
            msg = message_confirmation(user.id, user.email, user.confirmation_string)
            mail.send(msg)
            flash(_('Confirmation message sent, check your e-mail'))
            return redirect('')
        elif form.problem.data == 'password':
            new_password = random_string(10)
            user.password = password_hash(new_password)
            db.session.commit()
            msg = message_reset_password(user.email, new_password)
            mail.send(msg)
            flash(_('Your password was reset, check your e-mail'))
            return redirect('')

    return render_template('account_problem.html', form=form)


if __name__ == '__main__':
    app.run()

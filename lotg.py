from flask import Flask, render_template, g, session, request
from flask.ext.babel import Babel

from config import LANGUAGES
from models import db
from forms import SignInForm, SignUpForm

app = Flask(__name__)
app.config.from_object('config')

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
        return 'Success'
    return render_template('sign_up.html', form=form)


if __name__ == '__main__':
    app.run()

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired
from flask.ext.babel import lazy_gettext as _


class SignInForm(Form):
    email = StringField(_('E-mail'), validators=[DataRequired(), Email()])
    password = PasswordField(_('Password'), validators=[DataRequired()])

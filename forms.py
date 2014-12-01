from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired
from flask.ext.babel import lazy_gettext as _

# Common messages
msg_required = _('Field is required')
msg_email = _('Must be valid e-mail address')


class SignInForm(Form):
    email = StringField(_('E-mail'), validators=[DataRequired(msg_required), Email(msg_email)])
    password = PasswordField(_('Password'), validators=[DataRequired(msg_required)])

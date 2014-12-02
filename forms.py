from flask_wtf import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import Email, DataRequired, EqualTo, Length, Optional
from flask.ext.babel import lazy_gettext as _
from config import LANGUAGES, BABEL_DEFAULT_TIMEZONE

# Common validation messages
msg_required = _('Field is required')
msg_email = _('Must be valid e-mail address')


def msg_length_max(n):
    return _('Maximum length is %(max)d', max=n)


def msg_length_min(n):
    return _('Minimum length is %(min)d', min=n)


class SignInForm(Form):
    email = StringField(_('E-mail'), validators=[DataRequired(msg_required), Email(msg_email)])
    password = PasswordField(_('Password'), validators=[DataRequired(msg_required),
                                                        Length(min=6, message=msg_length_min(6))])


class SignUpForm(SignInForm):
    password_confirmation = PasswordField(_('Confirm password'),
                                          validators=[DataRequired(msg_required),
                                                      EqualTo('password',
                                                              message=_('Password and confirmation must be equal'))])
    language = SelectField(_('Language'), choices=LANGUAGES.items())
    timezone = StringField(_('Timezone'), default=BABEL_DEFAULT_TIMEZONE,
                           validators=[DataRequired(msg_required), Length(max=50, message=msg_length_max(50))])

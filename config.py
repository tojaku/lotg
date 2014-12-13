import private

DEBUG = True
SITE_NAME = 'Lord of the Games'
SECRET_KEY = 'ov:U7>9*D1/S0&Zf$#7E1@a,t.jF-U+Q'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://' + private.MYSQL_USERNAME + ':'\
                          + private.MYSQL_PASSWORD + '@localhost:3306/lotgpy'

BABEL_DEFAULT_LOCALE = 'hr'
BABEL_DEFAULT_TIMEZONE = 'Europe/Zagreb'
LANGUAGES = {
    'hr': 'Hrvatski',
    'en': 'English'
}

# MAIL SETTINGS
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME = private.MAIL_USERNAME
MAIL_PASSWORD = private.MAIL_PASSWORD
DEFAULT_MAIL_SENDER = 'admin@lordofthegames.eu'
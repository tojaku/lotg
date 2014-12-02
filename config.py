import private

DEBUG = True
SECRET_KEY = 'ov:U7>9*D1/S0&Zf$#7E1@a,t.jF-U+Q'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://' % private.MYSQL_USERNAME % ':'\
                          % private.MYSQL_PASSWORD % '@localhost:3306/lotgpy'
BABEL_DEFAULT_LOCALE = 'hr'
BABEL_DEFAULT_TIMEZONE = 'Europe/Zagreb'
LANGUAGES = {
    'hr': 'Hrvatski',
    'en': 'English'
}
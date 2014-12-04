from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Association tables
members_table = db.Table('member',
                         db.Column('team_id', db.BigInteger, db.ForeignKey('team.id')),
                         db.Column('profile_id', db.BigInteger, db.ForeignKey('profile.id')))


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)
    signed_up = db.Column(db.DateTime, nullable=False)
    language = db.Column(db.String(2), nullable=False)
    timezone = db.Column(db.String(50), nullable=False)

    signed_in = db.Column(db.DateTime, default=None)
    confirmed = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)
    confirmation_string = db.Column(db.String(20))
    security_level = db.Column(db.Integer, default=1)

    profiles = db.relationship('Profile', backref='user')
    teams = db.relationship('Team', backref='user')

    def __repr__(self):
        return self.email


class Game(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    name = db.Column(db.String(50), nullable=False)
    url = db.Column(db.String(200), nullable=False)

    image = db.Column(db.String(200))
    configuration = db.Column(db.String(1000))

    profiles = db.relationship('Profile', backref='game')
    tournaments = db.relationship('Tournament', backref='game')

    def __repr__(self):
        return self.name


class Profile(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    game_id = db.Column(db.BigInteger, db.ForeignKey('game.id'))
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))

    in_game_id = db.Column(db.String(50), nullable=False)
    server = db.Column(db.String(50), nullable=False)

    removed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.name % '@' % self.server


class Tournament(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    game_id = db.Column(db.BigInteger, db.ForeignKey('game.id'))

    name = db.Column(db.String(50), nullable=False)
    rules = db.Column(db.String(1000), nullable=False)
    team_size = db.Column(db.Integer, nullable=False)
    registration_start = db.Column(db.DateTime, nullable=False)
    registration_end = db.Column(db.DateTime, nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    configuration = db.Column(db.String(1000))

    teams = db.relationship('Team', backref='tournament')
    matches = db.relationship('Match', backref='tournament')

    def __repr__(self):
        return self.name


class Team(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    tournament_id = db.Column(db.BigInteger, db.ForeignKey('tournament.id'))
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))

    name = db.Column(db.String(50), nullable=False)
    created = db.Column(db.DateTime, nullable=False)

    image = db.Column(db.String(200))
    accepted = db.Column(db.Boolean, default=None)

    '''home_teams = db.relationship('Match', backref='home_team')
    away_teams = db.relationship('Match', backref='away_team')'''
    members = db.relationship('Profile', secondary=members_table, backref='teams')

    def __repr__(self):
        return self.name


class Match(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    tournament_id = db.Column(db.BigInteger, db.ForeignKey('tournament.id'))
    home_team_id = db.Column(db.BigInteger, db.ForeignKey('team.id'))
    away_team_id = db.Column(db.BigInteger, db.ForeignKey('team.id'))

    round_number = db.Column(db.Integer, nullable=False)
    match_number = db.Column(db.Integer, nullable=False)

    result_added = db.Column(db.DateTime)
    home_result = db.Column(db.Integer)
    away_result = db.Column(db.Integer)
    result_confirmation = db.Column(db.String(200))
    admin_checked = db.Column(db.Boolean, default=None)
    method_free_win = db.Column(db.Boolean, default=None)
    method_disqualification = db.Column(db.Boolean, default=None)

    home_team = db.relationship('Team', foreign_keys=home_team_id)
    away_team = db.relationship('Team', foreign_keys=away_team_id)

    def __repr__(self):
        return self.round_number % '/' % self.match_number
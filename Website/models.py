#we want a database model for our notes and our users
#you are importing sqlalchemy
from . import db
from flask_login import UserMixin
# from flask_admin import RoleMixin
from sqlalchemy.sql import func
from dataclasses import dataclass

@dataclass()
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    #Player logic - note is the child where player is the parent
    playerId = db.Column(db.Integer, db.ForeignKey('player.id'), nullable=False)
    player = db.relationship("Player", back_populates="notes")
    #Coach logic - note is the child coach is the parent
    coachId = db.Column(db.Integer, db.ForeignKey('coach.id'), nullable=False)
    coach = db.relationship("Player", back_populates="notes")
    #Note Type Logic
    noteTypeId = db.Column(db.Integer, db.ForeignKey('notetype.id'), nullable=False)
    noteType = db.relationship("Notetype", back_populates="notes")

@dataclass()
class Notetype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    notes = db.relationship('Note', back_populates="noteType")

    def get_id(self):
        return self.id

# Define the Role data-model
# @dataclass()
# class Role(db.Model):
#     __tablename__ = 'roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(50), unique=True)
#
# @dataclass()
# class UserRoles(db.Model):
#     __tablename__ = 'user_roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

@dataclass()
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.relationship('Role', secondary='user_roles')
    # confirmed_at = db.Column(db.DateTime(), nullable=True)
    #These are the 1 to 1 relationships
    adminn = db.relationship("Adminn", back_populates="user", uselist=False)
    player = db.relationship("Player", back_populates="user", uselist=False)
    coach = db.relationship("Coach", back_populates="user", uselist=False)

@dataclass()
class Player(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    #Relevant Player Data
    dob = db.Column(db.DateTime(timezone=False))
    height = db.Column(db.String(5), nullable=True)
    weight = db.Column(db.Float(3), nullable=True)
    shootDir = db.Column(db.String(5), nullable=True)
    position = db.Column(db.String(15), nullable=True)
    #user id relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="player")
    #Note relationship
    notes = db.relationship('Note', back_populates="player")
    #Coach is the parent, many to one
    coachId = db.Column(db.Integer, db.ForeignKey('coach.id'))
    coach = db.relationship('Coach', back_populates="player")
    #Team info - player is child
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))
    team = db.relationship('Team', back_populates="player")
    rating = db.relationship('Rating', back_populates="player")

@dataclass()
class Adminn(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #Still a many to 1 - actual constraints need to be made in the actual database schema
    user = db.relationship("User", back_populates="adminn")

@dataclass()
class Coach(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    assnCoach = db.Column(db.Boolean, default=False)
    #user id relationship
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", back_populates="coach")
    #Player relationship - coach is parent, one to many
    player = db.relationship("Player", back_populates="coach")
    #Team stuff
    #One team has multiple coaches there fore one to many, coach is the child
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))
    team = db.relationship('Team', back_populates="coach")
    rating = db.relationship('Rating', back_populates="coach")


@dataclass()
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamName = db.Column(db.String(50), nullable=False)
    coach = db.relationship("Coach", back_populates="team")
    player = db.relationship('Player', back_populates="team")
    gameId = db.Column(db.Integer, db.ForeignKey('game.id'))
    game = db.relationship('Game', back_populates="team")

@dataclass()
class Game(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    opponent = db.Column(db.String(150), unique=False, nullable=True)
    homeGame = db.Column(db.Boolean, nullable=False)
    location = db.Column(db.String(150), nullable=True)
    date = db.Column(db.DateTime(timezone=False))
    playoff = db.Column(db.Boolean, nullable=False)
    homeTeamScore = db.Column(db.Integer, nullable=True)
    awayTeamScore = db.Column(db.Integer, nullable=True)
    team = db.relationship('Team', back_populates="game")


@dataclass()
class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.relationship('Rating', back_populates="metric")


@dataclass()
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    value = db.Column(db.Integer, nullable=True)
    authorId = db.Column(db.Integer, nullable=False)
    #Metric many to one
    metricId = db.Column(db.Integer, db.ForeignKey('metric.id'))
    metric = db.relationship('Metric', back_populates="rating")
    #player many to one
    playerId = db.Column(db.Integer, db.ForeignKey('player.id'))
    player = db.relationship('Player', back_populates="rating")
    coachId = db.Column(db.Integer, db.ForeignKey('coach.id'))
    coach = db.relationship('Coach', back_populates="rating")







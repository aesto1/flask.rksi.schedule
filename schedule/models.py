from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=False)
    password = db.Column(db.String(200), primary_key=False, unique=False, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Teacher(db.Model):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    schedules = db.relationship('Schedule', backref='teacher')

    def __repr__(self):
        return '{}'.format(self.name)

class Group(db.Model):
    __tablename__ = 'groups'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    schedules = db.relationship('Schedule', backref='group')


    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return '{}'.format(self.name)

class Weekday(db.Model):
    __tablename__ = 'weekdays'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    wdid = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    schedules = db.relationship('Schedule', backref='weekday')

class Schedule(db.Model):
    __tablename__ = 'schedule'
    
    id = db.Column(db.Integer, primary_key=True)

    group_id = db.Column(db.Integer, db.ForeignKey(Group.id))
    teacher_id = db.Column(db.Integer, db.ForeignKey(Teacher.id))
    weekday_id = db.Column(db.Integer, db.ForeignKey(Weekday.id))
    lesson_name = db.Column(db.String(100))
    time_start = db.Column(db.String)
    time_end = db.Column(db.String)
    time = db.Column(db.Integer)
    week = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    auditory_name = db.Column(db.String)
    
    def __repr__(self):
        return str(self.group_id)
    
    def __str__(self):
        return self.lesson_name


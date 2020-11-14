from flask import Blueprint, render_template, redirect, abort, request, url_for, session
from flask_login import current_user
from flask import current_app
from . import db
from .models import Group, Teacher, Schedule, Weekday
import json
from datetime import datetime, timedelta, date

main = Blueprint('main', __name__)


@main.route('/')
def mainpage():
    gs = Group.query.all()
    ts = Teacher.query.all()
    return render_template('main.html', gs=gs, ts=ts)


@main.route('/schedule')
def getschedulegroup():
    if 'group' in request.args:
        g = request.args.get('group')
        g = Group.query.filter_by(name=g).first()
        gs = Group.query.all()
        ts = Teacher.query.all()
        
        rasp = Schedule.query.filter_by(group=g)
        week = Weekday.query.filter( Weekday.date>=datetime.combine( date.today(), datetime.min.time() ), Weekday.date<=(datetime.now()+timedelta(days=7)) )
        grdays = {}
        for l in rasp:
            grdays[l.weekday_id] = 1
        session.permanent = True
        session['group'] = g.id
        return render_template('main.html', week=week, sched = rasp, gs=gs, ts=ts, grdays=grdays, objname=g.name)
    if 'teacher' in request.args:
        t = request.args.get('teacher')
        t = Teacher.query.filter_by(name=t).first()
        gs = Group.query.all()
        ts = Teacher.query.all()
        rasp = Schedule.query.filter_by(teacher=t)
        week = Weekday.query.filter( Weekday.date>=datetime.combine( date.today(), datetime.min.time() ), Weekday.date<=(datetime.now()+timedelta(days=7)) )
        grdays = {}
        for l in rasp:
            grdays[l.weekday_id] = 1
        session.permanent = True
        session['teacher'] = t.id
        return render_template('main.html', week=week, sched = rasp, gs=gs, ts=ts, grdays=grdays, objname=t.name)
    else:
        return redirect(url_for('main.mainpage'))


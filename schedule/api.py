from flask import Blueprint, current_app
import json
from datetime import datetime, timedelta, date
from . import db
from .models import Group, Teacher, Weekday, Schedule

api = Blueprint('api', __name__)

@api.route('/api/iphone/today/<group>')
def api_iphone_today(group):
    g = Group.query.filter_by(name=group).first()
    week = Weekday.query.filter_by(date = (datetime.combine(date.today(), datetime.min.time()))).first()  
    rasp = Schedule.query.filter_by(group=g).all()
    # current_app.logger.info("{}.{}".format(week.date.day, week.date.month))
    grdays = {}
    for l in rasp:
        grdays[l.weekday_id] = 1
    # current_app.logger.info("{}".format(grdays))
    if not week: return "Сегодня выходной!"
    if week.wdid not in grdays: return "Сегодня выходной!"
    
    r = ""
    for lesson in rasp:
        # current_app.logger.info("{} : {}".format(lesson.date.day, datetime.today().day))
        if lesson.date.day == datetime.today().day:
            r+="{}.{} {} — {}, {} - ауд.{}<br>".format(lesson.time, lesson.lesson_name, lesson.time_start, lesson.time_end, lesson.teacher.name, lesson.auditory_name)
    return r


@api.route('/api/iphone/tomorrow/<group>')
def api_iphone_tomorrow(group):
    g = Group.query.filter_by(name=group).first()
    week = Weekday.query.filter_by(date = (datetime.combine(date.today(), datetime.min.time()))+timedelta(days=1)).first()  
    rasp = Schedule.query.filter_by(group=g).all()
    # current_app.logger.info("{}.{}".format(week.date.day, week.date.month))
    grdays = {}
    for l in rasp:
        grdays[l.weekday_id] = 1
    # current_app.logger.info("{}".format(grdays))
    if not week: return "Завтра выходной!"
    if week.wdid not in grdays: return "Завтра выходной!"
    
    r = ""
    for lesson in rasp:
        # current_app.logger.info("{} : {}".format(lesson.date.day, datetime.today().day))
        if lesson.date.day == (datetime.today()+timedelta(days=1)).day:
            r+="{}.{} {} — {}, {} - ауд.{}<br>".format(lesson.time, lesson.lesson_name, lesson.time_start, lesson.time_end, lesson.teacher.name, lesson.auditory_name)
    return r



@api.route('/api/json/groups')
def api_groups():
    g = Group.query.all()
    return str(g)

@api.route('/api/json/teachers')
def api_teachers():
    t = Teacher.query.all()
    return str(t)
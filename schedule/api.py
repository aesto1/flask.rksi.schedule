from flask import Blueprint, current_app, request, jsonify, Response
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


@api.route('/api/json/schedule/group', methods=['POST'])
def api_group_schedule():
    weekdays = [1, 2, 3, 4, 5, 6]
    j = {'schedule': {'days' : {}}}
    wdavailable = [-1, 0, 1, 2, 3, 4, 5, 6]
    r = request.json
    if 'group' not in r:
        return json.dumps({'error': 'group value is missed'})
    else:
        g = Group.query.filter_by(name = r['group']).first()
    if 'weekday' in r:
        if r['weekday'] in wdavailable:
            # Вывести все дни недели этой недели
            if r['weekday'] == -1:
                wdtoday = Weekday.query.filter_by(date=datetime.combine(date.today(), datetime.min.time())).first()
                if wdtoday:
                    pass
                else:
                    wdtoday = Weekday.query.filter_by(date=datetime.combine((date.today()+timedelta(days=1)), datetime.min.time())).first()
                s = Schedule.query.filter_by(group=g, week=wdtoday.week).all()
                for d in s:
                    if d.weekday.name not in j['schedule']['days']: j['schedule']['days'][d.weekday.name] = {}
                for day in weekdays:
                    for l in s:
                        if l.weekday.wdid == day:
                            j['schedule']['days'][l.weekday.name][int(l.time)] = {'lesson_name': l.lesson_name, 'time_start':l.time_start, 'time_end':l.time_end, 'autitory':l.auditory_name, 'teacher':l.teacher.name}
                return Response(response=json.dumps(j, ensure_ascii=False), status=200, mimetype='application/json')
                

            # Вывести 7 дней начиная с сегодня
            elif r['weekday'] == 0:
                week = Weekday.query.filter( Weekday.date>=datetime.combine( date.today(), datetime.min.time() ), Weekday.date<=(datetime.now()+timedelta(days=7)) ).all()
                rasp = Schedule.query.filter(Schedule.week>=week[0].week).filter_by(group=g).all()
                for w in week:
                    for l in rasp:
                        if l.weekday.wdid == w.wdid:
                            wdate = w.date
                            return "{} {} {}".format(wdate.day, wdate.month, wdate.year)
                            # ЭТО БЛЯТЬ ДЕРЬМО НЕ РАБОТАЕТ!!!!:(
                            if "{}-{}-{}".format(wdate.day, wdate.month, wdate.year) not in j['schedule']['days']: j['schedule']['days']["{}-{}-{}".format(wdate.day, wdate.month, wdate.year)] = {}
                            j['schedule']['days']["{}-{}-{}".format(wdate.day, wdate.month, wdate.year)][int(l.time)] = {'lesson_name': l.lesson_name, 'time_start':l.time_start, 'time_end':l.time_end, 'autitory':l.auditory_name, 'teacher':l.teacher.name}
                return Response(response=json.dumps(j, ensure_ascii=False), status=200, mimetype='application/json')
            elif r['weekday'] >=1:
                pass
                # Вывести конкретный день недели 
        else:
            return json.dumps({'error': 'weekday value is wrong'})
    return str(r)

@api.route('/api/json/list/groups', methods=['POST'])
def api_allgroups():
    g = Group.query.all()
    j = { 'list': {} } 
    i=0
    for group in g:
        j['list'][int(i)] = group.name
        i+=1
    return json.dumps(j, ensure_ascii=False)

@api.route('/api/json/list/teachers', methods=['POST'])
def api_allteachers():
    t = Teacher.query.all()
    j = {'list': {} } 
    i=0
    for teacher in t:
        j['list'][int(i)] = teacher.name
        i+=1
    return json.dumps(j, ensure_ascii=False)
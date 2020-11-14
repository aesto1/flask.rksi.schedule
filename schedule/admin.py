from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask import current_app
from flask_login import login_required
import logging
from . import db
from .models import User, Group, Schedule, Teacher, Weekday

import random
import string
from datetime import datetime as dt
import datetime
import json
import requests
import sys
sys.setrecursionlimit(10000)
admin = Blueprint('admin', __name__)

@admin.route('/adminpanel')
@login_required
def adminpanel():
   return render_template('admin.html')


@admin.route('/admin/weekday/drop', methods=['POST'])
@login_required
def dropweekday():
    db.session.query(Weekday).delete()
    db.session.commit()
    flash('Таблица Weekdays очищена!')
    return redirect(url_for('admin.adminpanel'))

@admin.route('/admin/groups/drop', methods=['POST'])
@login_required
def dropgroups():
    db.session.query(Group).delete()
    db.session.commit()
    flash('Таблица Groups очищена!')
    return redirect(url_for('admin.adminpanel'))

@admin.route('/admin/teachers/drop', methods=['POST'])
@login_required
def dropteachers():
    db.session.query(Teacher).delete()
    db.session.commit()
    flash('Таблица Teachers очищена!')
    return redirect(url_for('admin.adminpanel'))

@admin.route('/admin/schedule/drop', methods=['POST'])
@login_required
def dropschedule():
    db.session.query(Schedule).delete()
    db.session.commit()
    flash('Таблица Schedule очищена!')
    return redirect(url_for('admin.adminpanel'))

@admin.route('/admin/weekday/update', methods=['POST'])
@login_required
def updateweekday():
    url = "https://rksi.ru/rasp/r.json"
    r = requests.get(url)
    j = json.loads(r.text)
    gs = j['faculties'][0]['groups']
    for gr in gs:
        for day in gr['days']:
            if 'lessons' in day:
                for lesson in day['lessons']:
                    if not Weekday.query.filter_by(wdid = int(day['weekday']), date = dt.strptime(lesson['date'], "%d-%m-%Y")).first():
                        if int(day['weekday'])==1: wdname = "Понедельник"
                        if int(day['weekday'])==2: wdname = "Вторник"
                        if int(day['weekday'])==3: wdname = "Среда"
                        if int(day['weekday'])==4: wdname = "Четверг"
                        if int(day['weekday'])==5: wdname = "Пятница"
                        if int(day['weekday'])==6: wdname = "Суббота"
                        if int(day['weekday'])==7: wdname = 'Воскресенье'
                        datestrp = dt.strptime(lesson['date'], "%d-%m-%Y")
                        w = Weekday(name=wdname, wdid = int(day['weekday']), date = datestrp, week=lesson['week'])
                        db.session.add(w)
                        current_app.logger.info('{} {}.{}.{} added!'.format(w.name, w.date.day, w.date.month, w.date.year))
    db.session.commit()
    return redirect(url_for('admin.adminpanel'))

@admin.route('/admin/groups/update', methods=['POST'])
@login_required
def updategroups():
    url = "https://rksi.ru/export/schedule.php?type=groups"
    r = requests.get(url)
    l = (r.text.encode().decode('unicode_escape')
                                                ).replace("'", ""
                                                ).replace('"', ""
                                                ).replace("]", ""
                                                ).replace("[", ""
                                                ).split(',')
    for group in l:
        if not Group.query.filter_by(name=group):
            g = Group(name=group).first()
            db.session.add(g)
            current_app.logger.info("UPDATEGROUP: {} added!".format(group))
        else:
            continue
    db.session.commit()
    return redirect(url_for('admin.adminpanel'))

@admin.route('/admin/teachers/update', methods=['POST'])
@login_required
def updateteachers():
    url = "https://rksi.ru/export/schedule.php?type=teachers"
    r = requests.get(url)
    l = (r.text.encode().decode('unicode_escape')
                                                ).replace("'", ""
                                                ).replace('"', ""
                                                ).replace("]", ""
                                                ).replace("[", ""
                                                ).split(',')
    for teacher in l:
        if not Teacher.query.filter_by(name=teacher).first():
            g = Teacher(name=teacher)
            db.session.add(g)
            current_app.logger.info("UPDATETEACHER: {} added!".format(teacher))
        else:
            continue
    db.session.commit()
    return redirect(url_for('admin.adminpanel'))

@admin.route('/admin/schedule/update', methods=['POST'])
@login_required
def updateschedule():
    url = "https://rksi.ru/rasp/r.json"
    r = requests.get(url)
    j = json.loads(r.text)
    gs = j['faculties'][0]['groups']
    for gr in gs:
        for day in gr['days']:
            if 'lessons' in day:
                for lesson in day['lessons']:
                    g = Group.query.filter_by(name=str(gr['group_name'])).first()
                    if not Schedule.query.filter_by(group=g ,lesson_name = lesson['subject'], time=int(lesson['time']), date = dt.strptime(lesson['date'], "%d-%m-%Y")).first():
                        g = Group.query.filter_by(name=str(gr['group_name'])).first()
                        t = Teacher.query.filter_by(name=lesson['teachers'][0]['teacher_name']).first()
                        w = Weekday.query.filter_by(wdid = int(day['weekday']), date = dt.strptime(lesson['date'], "%d-%m-%Y")).first()
                        s = Schedule(
                            group = g,
                            teacher = t,
                            weekday = w,
                            lesson_name = lesson['subject'],
                            time_start = lesson['time_start'],
                            time_end = lesson['time_end'],
                            time = int(lesson['time']),
                            week = int(lesson['week']),
                            date = dt.strptime(lesson['date'], "%d-%m-%Y"),
                            auditory_name = str(lesson['auditories'][0]['auditory_name'])
                            )
                        db.session.add(s)
                        current_app.logger.info("UPDATESCHEDULE: {}.{}.{} - {} {}-пара added!".format(s.date.day, s.date.month, s.date.year, s.group.name, s.time))
    db.session.commit()
    return redirect(url_for('admin.adminpanel'))
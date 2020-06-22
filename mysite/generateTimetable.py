import http.client
import json
import threading
import time
import schedule

from enum import IntEnum
from django.contrib.auth.models import Group

from timetable.models import dayOfWeek, Lesson, HourLesson
from timetable.views import setTimetable4day, createHourLessons, setTimetable4dayfromAPI


codeGroups = {
    "eng1": Group.objects.get(name="English Group 1").id,
    "eng2": Group.objects.get(name="English Group 2").id,
    "grm1": Group.objects.get(name="Germany Group 1").id,
    "grm2": Group.objects.get(name="Germany Group 2").id,
    "prac1": Group.objects.get(name="utk1").id,
    "prac2": Group.objects.get(name="utk2").id,
    "prac3": Group.objects.get(name="utk3").id,
    "wf1": Group.objects.get(name="wf1").id,
    "wf2": Group.objects.get(name="wf2").id,
    "wf3": Group.objects.get(name="wfGirls").id
}


def changeGroup(obj):
    if obj['groupNum'] == 0:
        obj['group'] = -1
        return obj
    if obj['group'] in codeGroups:
        obj['group'] = codeGroups[str(obj['group'])]
    elif obj['subject'] == "j.nie":
        obj['group'] = codeGroups["grm" + str(obj['groupNum'])]
    elif obj['subject'] == "wf":
        obj['group'] = codeGroups["wf" + str(obj['groupNum'])]
    else:
        obj['group'] = codeGroups["eng" + str(obj['groupNum'])]
    return obj


def updatingTimetable():
    try:
        conn = http.client.HTTPSConnection("plan.zsll.ga")
        conn.request("GET", "/api/timetable/0/get/1i2")
        res = conn.getresponse()
        data = json.loads(res.read())
    except Exception as e:
        print("Cannot get data from plan.zsll.ga :")
        print(e)
        return
    HourLesson.objects.all().delete()

    for hour in data['periods']:
        createHourLessons(hour, hour['num'])

    Lesson.objects.all().delete()
    for day in dayOfWeek.choices():
        setTimetable4dayfromAPI(data[day[1].lower()], day, changeGroup)


def treadFunction():
    updatingTimetable()
    schedule.every(16).hours.do(updatingTimetable)

    while True:
        schedule.run_pending()
        time.sleep(10)

def startTreading():
    thread = threading.Thread(target=treadFunction)
    thread.start()

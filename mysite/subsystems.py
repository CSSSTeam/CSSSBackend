import http.client
import json
import threading
import time
from enum import IntEnum

import schedule

from timetable.models import dayOfWeek, Lesson, HourLesson
from timetable.views import setTimetable4day, createHourLessons, setTimetable4dayfromAPI

codeGroups = {
    0: -1,
    1: 1,
    2: 3,
    3: 4,
}


def changeGroup(obj):
    obj.group = codeGroups[obj['groupNum']]
    return obj


def updatingTimetable():
    conn = http.client.HTTPSConnection("plan.zsll.ga")
    conn.request("GET", "/api/timetable/9/get/1i2")
    res = conn.getresponse()
    data = json.loads(res.read())
    # print(data)
    HourLesson.objects.all().delete()
    print(data)

    for hour in data['periods']:
        createHourLessons(hour, hour['num'])

    Lesson.objects.all().delete()
    for day in dayOfWeek.choices():
        setTimetable4dayfromAPI(data[day[1].lower()], day,codeGroups)


def treadFunction():
    updatingTimetable()
    schedule.every(1).minutes.do(updatingTimetable)

    while True:
        schedule.run_pending()
        time.sleep(10)


thread = threading.Thread(target=treadFunction)
thread.start()

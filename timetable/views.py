from django.contrib.auth.models import Group
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from timetable.models import HourLesson, Lesson
from datetime import timedelta
import json
from timetable.models import dayOfWeek


# Create your views here.
@api_view(['GET'])
def getTimetable(request):
    response = {"period": []}
    hourLessons = HourLesson.objects.all().order_by("number")
    for period in hourLessons:
        response["period"].append({'start': period.start, 'end': period.end})

    for day in dayOfWeek.choises():
        dayLessons = []
        lessonsData = Lesson.objects.filter(day=day[0])
        for hour in hourLessons:
            lesson = []
            lessonData = lessonsData.filter(hour=hour)
            for l in lessonData:
                lesson.append({"name": l.name, "group": l.group})
            dayLessons.append(lesson)
        response[day[1].lower()] = dayLessons
    return Response(response)


# TODO(n2one): create poemision for setTimetable
@api_view(['POST'])
def setTimetable(request):
    timetable = json.loads(request.body)
    for day in dayOfWeek.choises():
        if not timetable[day[1].lower()] is None:
            Lesson.objects.filter(day=day[0]).delete()
            setTimetable4day(timetable[day[1].lower()], day)
    return Response("OK")


def setTimetable4day(lessonsOfDay, day):
    num_lesson = 0
    for lessonData in lessonsOfDay:
        hour = HourLesson.objects.get(number=num_lesson)
        for l in lessonData:
            lesson = Lesson(name=l["name"], day=day[0], hour=hour, group=l["group"])
            lesson.save()
        num_lesson = num_lesson + 1


# TODO(n2one):create permisions for setHourLessons
@api_view(['POST'])
def setHourLessons(request):
    body = json.loads(request.body)
    HourLesson.objects.all().delete()
    num_lesson = 0
    for obj in body:
        createHourLessons(obj, num_lesson)
        num_lesson = num_lesson + 1
    return Response("OK")


def createHourLessons(lessonObject, num_lesson):
    lesson = HourLesson(number=num_lesson, start=lessonObject['start'], end=lessonObject['end'])
    lesson.save()
    return lesson

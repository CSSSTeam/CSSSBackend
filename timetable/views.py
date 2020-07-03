import json
from datetime import timedelta

from django.contrib.auth.models import Group
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from timetable.models import HourLesson, Lesson, dayOfWeek
from timetable.permission import (canGetTimetable, canSetHourLesson,
                                  canSetTimetable)
from users.utility import getUser


@api_view(['GET'])
@permission_classes([canGetTimetable])
def getTimetable(request):
    response = {"period": []}
    hourLessons = HourLesson.objects.all().order_by("number")
    for period in hourLessons:
        response["period"].append({'num': period.number, 'start': period.start, 'end': period.end})

    for day in dayOfWeek.choices():
        dayLessons = []
        lessonsData = Lesson.objects.filter(day=day[0])
        for hour in hourLessons:
            lesson = []
            lessonData = lessonsData.filter(hour=hour)
            for l in lessonData:
                lesson.append({"subject": l.subject, "classroom": l.classroom, "teacher": l.teacher, "group": l.group})
            dayLessons.append(lesson)
        response[day[1].lower()] = dayLessons
    return Response(response)


@api_view(['GET'])
@permission_classes([canGetTimetable])
def getMyTimetable(request):
    user = getUser(request)
    response = {"period": []}
    hourLessons = HourLesson.objects.all().order_by("number")
    for period in hourLessons:
        response["period"].append({'num': period.number, 'start': period.start, 'end': period.end})

    for day in dayOfWeek.choices():
        dayLessons = []
        lessonsData = Lesson.objects.filter(day=day[0])
        for hour in hourLessons:
            lesson = []

            lessonData = lessonsData.filter(hour=hour)
            for l in lessonData:
                if l.group == -1 or user.groups.filter(id=l.group).exists():
                    lesson.append(
                        {"subject": l.subject, "classroom": l.classroom, "teacher": l.teacher, "group": l.group})
                    break
            dayLessons.append(lesson)
        response[day[1].lower()] = dayLessons
    return Response(response)


@api_view(['POST'])
@permission_classes([canSetTimetable])
def setTimetable(request):
    timetable = json.loads(request.body)
    for day in dayOfWeek.choises():
        if not timetable[day[1].lower()] is None:
            Lesson.objects.filter(day=day[0]).delete()
            try:
                setTimetable4day(timetable[day[1].lower()], day)
            except Exception as exeption:
                return Response({"error": str(exeption)}, status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_201_CREATED)


def setTimetable4day(lessonsOfDay, day):
    num_lesson = 0
    for lessonsData in lessonsOfDay:
        print(HourLesson.objects.all())
        hour = HourLesson.objects.get(number=num_lesson + 1)
        num_lesson = num_lesson + 1
        if lessonsData is None:
            continue
        for lessonData in lessonsData:
            if (not "subject" in lessonData) or lessonData['subject'] == "":
                raise Exception(f"lesson in {day[0]} time {num_lesson + 1} has not subject")
            if (not "teacher" in lessonData) or lessonData['teacher'] == "":
                raise Exception(f"lesson in {day[0]} time {num_lesson + 1} has not teacher")
            if (not "classroom" in lessonData) or lessonData['classroom'] == "":
                raise Exception(f"lesson in {day[0]} time {num_lesson + 1} has not classroom")
            if (not "group" in lessonData) or (
                    (not str(lessonData['group']) == "-1") and Group.objects.filter(id=lessonData['group']) is None):
                raise Exception(f"lesson in {day[0]} time {num_lesson + 1} has group that does not exist")
            lesson = Lesson(subject=lessonData["subject"], day=day[0], hour=hour, teacher=lessonData["teacher"],
                            classroom=lessonData["classroom"],
                            group=lessonData["group"])
            lesson.save()


def setTimetable4dayfromAPI(lessonsOfDay, day, codeGroups):
    num_lesson = 0
    for lessonsData in lessonsOfDay:
        hour = HourLesson.objects.get(number=num_lesson + 1)
        num_lesson = num_lesson + 1
        if lessonsData is None:
            continue
        for lessonData in lessonsData:
            group = codeGroups(lessonData)['group']
            lesson = Lesson(subject=lessonData["subject"], day=day[0], hour=hour, teacher=lessonData["teacher"],
                            classroom=lessonData["classroom"],
                            group=group)
            lesson.save()


@api_view(['POST'])
@permission_classes([canSetHourLesson])
def setHourLessons(request):
    body = json.loads(request.body)
    HourLesson.objects.all().delete()
    num_lesson = 0
    for obj in body:
        try:
            createHourLessons(obj, num_lesson)
        except Exception as exeption:
            return Response({"error": str(exeption)}, status=status.HTTP_400_BAD_REQUEST)
        num_lesson = num_lesson + 1
    return Response(status=status.HTTP_201_CREATED)


def createHourLessons(lessonObject, num_lesson):
    if (not "start" in lessonObject) or lessonObject['start'] == "":
        raise Exception(f"Hour {num_lesson + 1} has not start")
    if (not "end" in lessonObject) or lessonObject['end'] == "":
        raise Exception(f"Hour {num_lesson + 1} has not end")

    lesson = HourLesson(number=num_lesson, start=lessonObject['start'], end=lessonObject['end'])
    lesson.save()
    return lesson

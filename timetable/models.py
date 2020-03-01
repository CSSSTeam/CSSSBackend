from django.db import models
from enum import IntEnum
from django.contrib.auth.models import Group


class dayOfWeek(IntEnum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


# Create your models here.
class HourLesson(models.Model):
    number = models.IntegerField(default=1)
    start = models.TimeField()
    end = models.TimeField()


class Lesson(models.Model):
    subject = models.TextField()
    classroom = models.TextField(default="")
    teacher = models.TextField(default="")
    day = models.IntegerField(choices=dayOfWeek.choices(), default=dayOfWeek.MONDAY)
    hour = models.ForeignKey(HourLesson, on_delete=models.CASCADE, default=None)
    group = models.IntegerField(default=-1)

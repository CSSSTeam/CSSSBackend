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
    def choises(cls):
        return [(key.value, key.name) for key in cls]


# Create your models here.
class HourLesson(models.Model):
    number = models.IntegerField(default=1)
    start = models.TextField()
    end = models.TextField()


class Lesson(models.Model):
    name = models.TextField()
    classroom = models.TextField(default="")
    teacher = models.TextField(default="")
    day = models.IntegerField(choices=dayOfWeek.choises(), default=dayOfWeek.MONDAY)
    hour = models.ForeignKey(HourLesson, on_delete=models.CASCADE, default=None)
    group = models.IntegerField(default=-1)

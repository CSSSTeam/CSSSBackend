from django.db import models
from django.utils import timezone

class type (models.Model):
    name = models.CharField(max_length=50)


class event (models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    dateStart = models.DateTimeField(default=timezone.now)
    dateEnd = models.DateTimeField(default=timezone.now)
    eventType = models.ForeignKey('type', blank=True, null=True, on_delete=models.CASCADE, default='')
    group = models.ForeignKey('auth.group', blank=True, null=True, on_delete=models.CASCADE, default='')

    #class Meta:
    #    permissions = [
    #        ("show", "Can change the status of tasks"),
    #        ("create", "Can remove a task by setting its status as closed"),
    #    ]
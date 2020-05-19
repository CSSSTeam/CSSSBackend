from django.db import models
from django.utils import timezone
from django.db.models.signals import post_migrate

class type (models.Model):
    name = models.CharField(max_length=50)


class event (models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    dateStart = models.DateTimeField(default=timezone.now)
    dateEnd = models.DateTimeField(default=timezone.now)
    eventType = models.ForeignKey('type', blank=True, null=True, on_delete=models.CASCADE, default='')
    group = models.ForeignKey('auth.group', blank=True, null=True, on_delete=models.CASCADE, default='')
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_migrate
import uuid

class type (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=6,default='000000')


class event (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.TextField()
    dateStart = models.DateTimeField(default=timezone.now)
    dateEnd = models.DateTimeField(default=timezone.now)
    eventType = models.ForeignKey('type', blank=True, null=True, on_delete=models.CASCADE, default='')
    group = models.ForeignKey('auth.group', blank=True, null=True, on_delete=models.CASCADE, default='')
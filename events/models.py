import uuid

from django.db import models
from django.db.models.signals import post_migrate
from django.utils import timezone

from .validators import color


class type (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=6, validators=[color], default='000000')


class event (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.TextField(default='', blank=True, null=True)
    dateStart = models.DateTimeField(default=timezone.now)
    dateEnd = models.DateTimeField(default=timezone.now)
    eventType = models.ForeignKey('type', on_delete=models.CASCADE)
    group = models.ForeignKey('auth.group', blank=True, null=True, on_delete=models.CASCADE)

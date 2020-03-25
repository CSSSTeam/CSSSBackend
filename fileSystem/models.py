from django.db import models
from django.utils import timezone

class type (models.Model):
    name = models.CharField(max_length=50)


class file (models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    fileType = models.ForeignKey('type', blank=True, null=True, on_delete=models.CASCADE, default='')
    upload = models.CharField(default='', unique=True, max_length=255)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.CASCADE, default='')

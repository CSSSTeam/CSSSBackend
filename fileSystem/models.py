from django.db import models
from django.utils import timezone

class type (models.Model):
    name = models.CharField(max_length=50)


class file (models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    fileType = models.ForeignKey('type', blank=True, null=True, on_delete=models.CASCADE, default='')
    upload = models.TextField(default='', unique=True)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.CASCADE, default='')

    ##upload = models.FileField(upload_to=cerate_path(fileType), default='')

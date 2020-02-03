from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class types (models.Model):
    name = models.CharField(max_length=50)

class file (models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    fileType = models.ForeignKey('types', on_delete=models.CASCADE, default=types.objects.get(id=1))
    upload = models.TextField(default="")
    date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    #author = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=User.objects.get(id=1))

    ##upload = models.FileField(upload_to=cerate_path(fileType), default="")

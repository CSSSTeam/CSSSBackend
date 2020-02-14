from django.db import models
from django.utils import timezone

class types (models.Model):
    name = models.CharField(max_length=50)

def createDefault():
    try:
        t = types.objects.get(pk=1)
    except types.DoesNotExist:
        t = types.objects.create(pk=1,name="None")
        t.save()
    return t

class file (models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    fileType = models.ForeignKey('types', on_delete=models.CASCADE, default=createDefault()) # need to be default='' on migration
    upload = models.TextField(default="")
    date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    #author = models.ForeignKey('auth.User', on_delete=models.CASCADE, default='')

    ##upload = models.FileField(upload_to=cerate_path(fileType), default="")

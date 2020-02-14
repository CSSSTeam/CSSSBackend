from django.db import models
from django.utils import timezone

class type (models.Model):
    name = models.CharField(max_length=50)

    
def createDefault():
    try:
        t = type.objects.get(pk=1)
    except type.DoesNotExist:
        t = type.objects.create(pk=1,name="None")
        t.save()
    return t

class event (models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    dateStart = models.DateTimeField(blank=True, null=True, default=timezone.now)
    dateEnd = models.DateTimeField(blank=True, null=True, default=timezone.now)
    eventType = models.ForeignKey('type', on_delete=models.CASCADE, default=createDefault()) # need to be default='' on migration
    #group = models.ForeignKey('auth.group', on_delete=models.CASCADE, default='')
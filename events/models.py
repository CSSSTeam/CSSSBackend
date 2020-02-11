from django.db import models
from django.utils import timezone

class type (models.Model):
    name = models.CharField(max_length=50)

class event (models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    dateStart = models.DateTimeField(blank=True, null=True, default=timezone.now)
    dateEnd = models.DateTimeField(blank=True, null=True, default=timezone.now)
    eventType = models.ForeignKey('type', on_delete=models.CASCADE, default=type.objects.get(id=1))
    #group = models.ForeignKey('auth.group', on_delete=models.CASCADE, default='')
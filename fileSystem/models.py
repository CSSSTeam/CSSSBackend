from django.db import models
from django.utils import timezonehttps://github.com/CSSSTeam/CSSSBackend/pull/8/conflicts

class types (models.Model):
    name = models.CharField(max_length=50)

class file (models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    fileType = models.ForeignKey('types', on_delete=models.CASCADE, default='')
    upload = models.TextField(default="")
    date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    #author = models.ForeignKey('auth.User', on_delete=models.CASCADE, default='')

    ##upload = models.FileField(upload_to=cerate_path(fileType), default="")

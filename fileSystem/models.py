from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#this function create path to file
def cerate_path(Type):
    return '\\'+str(Type.name)


class types (models.Model):
    name = models.CharField(max_length=50)

class file (models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    fileType = models.ForeignKey('types', on_delete=models.CASCADE, default=types.objects.get(id=1))
    upload = models.FileField(upload_to=cerate_path(fileType), default="")
    date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    #author = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=User.objects.get(id=1))
    
    #this function return url to file
    def getUrl(self):
        return self.fileType.url()

    #on upload file
    def onUpload(self):
        self.date = timezone.now()
        self.save()



from django.db import models
from django.utils import timezone

#this function ceretwe path to file
def cerate_path(Type):
    return '\\'+str(Type.name)


class file (models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    fileType = models.ForeignKey('types', on_delete=models.CASCADE, default="")
    upload = models.FileField(upload_to=cerate_path(fileType))
    date = models.DateTimeField(blank=True, null=True, default=timezone.now)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    #this function return url to file
    def getUrl(self):
        return self.fileType.url()

    #on upload file
    def upload(self):
        self.date = timezone.now()
        self.save()


class types (models.Model):
    name = models.CharField(max_length=50)

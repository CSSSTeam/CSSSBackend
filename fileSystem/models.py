from django.db import models
from django.utils import timezone
from chunked_upload.models import ChunkedUpload
import uuid

class type(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)


class file(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    description = models.TextField(default='', blank=True, null=True)
    fileType = models.ForeignKey('type', on_delete=models.CASCADE)
    upload = models.CharField(unique=True, max_length=255)
    date = models.DateTimeField(default=timezone.now, editable=False)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)


MyChunkedUpload = ChunkedUpload
from django.db import models
from django.utils import timezone
import uuid


class List(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    date = models.DateTimeField(default=timezone.now, editable=False)
    cost = models.FloatField()


class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    isPay = models.BooleanField(default=False)
    treasurerList = models.ForeignKey('List', on_delete=models.CASCADE)

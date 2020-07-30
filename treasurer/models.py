from django.db import models
import uuid


class List(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(default="")
    cost = models.IntegerField(default=0)


class Member(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    isPay = models.BooleanField(default=False)
    treasurerList = models.ForeignKey('List', on_delete=models.CASCADE)

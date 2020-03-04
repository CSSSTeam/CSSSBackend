from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class TreasurerList(models.Model):
    name = models.TextField(default="")
    cost = models.IntegerField(default=0)


class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isPay = models.BooleanField(default=False)
    treasurerList = models.ForeignKey(TreasurerList, on_delete=models.CASCADE)

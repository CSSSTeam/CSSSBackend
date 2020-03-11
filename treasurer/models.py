from django.db import models


class List(models.Model):
    name = models.TextField(default="")
    cost = models.IntegerField(default=0)


class Member(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    isPay = models.BooleanField(default=False)
    treasurerList = models.ForeignKey('TreasurerList', on_delete=models.CASCADE)

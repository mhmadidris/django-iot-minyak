from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Minyak(models.Model):
    user = models.CharField(max_length=50)
    volume = models.IntegerField()

class Poin(models.Model):
    user = models.CharField(max_length=50,unique=True)
    poin = models.IntegerField(default=0)
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Lockers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    key = models.CharField(max_length=100, unique=True)
    status = models.BooleanField()

    def __str__(self):
        return self.name
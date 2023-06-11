from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=200, blank=True, default="None", null="True")
    def __str__(self):
        return self.username

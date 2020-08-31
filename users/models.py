from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
class DocketUser(AbstractUser):
    email = models.EmailField('Email address', unique=True)
    teacher = models.BooleanField(default=False)
    newuser = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password']

    def __str__(self):
        return f"{self.username}"

    def getinfo(self):
        ans = {
            "id": self.id,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "teacher": str(self.teacher),
            "newuser": str(self.newuser),
        }

        return ans

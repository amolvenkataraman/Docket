from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.
class DocketUser(AbstractUser):
    email = models.EmailField('Email address', unique=True)
    teacher = models.BooleanField(default=False)
    newuser = models.BooleanField(default=True)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password']

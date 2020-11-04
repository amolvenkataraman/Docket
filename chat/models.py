from django.db import models
from users.models import *

# Create your models here.
class Group_Direct_Message(models.Model):
    name = models.CharField(max_length=256)
    users = models.ManyToManyField(DocketUser)
    created = models.DateTimeField(auto_now=True)
    icon = models.ImageField(upload_to="group_dm_icons", blank=True, null=True)

class Direct_Message_Set(models.Model):
    users = models.ManyToManyField(DocketUser)
    file_no = models.IntegerField()
    messages = models.IntegerField(default=0)

class Group_Direct_Message_Set(models.Model):
    group_dm = models.ForeignKey(Group_Direct_Message, on_delete=models.PROTECT)
    file_no = models.IntegerField()
    messages = models.IntegerField(default=0)

class Message_Image(models.Model):
    image = models.ImageField(upload_to="chat_images")
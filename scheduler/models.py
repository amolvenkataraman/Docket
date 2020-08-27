from django.db import models
from users.models import DocketUser

# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=64, unique=True)
    teacher = models.ForeignKey(DocketUser, on_delete=models.SET("DELETED_USER"), related_name='class_teacher')
    students = models.ManyToManyField(DocketUser, related_name='class_student')
    #room = "LOL"
    scheduled_class = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}, Teacher: {self.teacher.username}"

    def getinfo(self):
        ans = {
            "id": self.id,
            "name": self.name,
            "teacher": self.teacher.username,
            "scheduled_class": self.scheduled_class,
            "active": self.active,
        }

        return ans

class Group(models.Model):
    name = models.CharField(max_length=64, unique=True)
    classes = models.ManyToManyField(Class, related_name='group_class')

    def __str__(self):
        return f"{self.name}"

class Invite(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    code = models.CharField(max_length=8)

    def __str__(self):
        return f"{self.code}, for {self.Class.name}"

    def getinfo(self):
        ans = {
            "id": self.id,
            "class": self.Class.getinfo(),
            "code": self.code,
        }
        return ans

class Assignment(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    deadline = models.DateTimeField(auto_now=False)
    url = models.URLField(null=True)
    description = models.TextField()
    graded = models.BooleanField(default=False)
    priority = models.SmallIntegerField(default=3)

    def __str__(self):
        return f"{self.name} for {self.Class.name}. Due: {str(self.deadline)}"

    def getinfo(self):
        ans = {
            "id": self.id,
            "class": self.Class.getinfo(),
            "name": self.name,
            "deadline": str(self.deadline),
            "url": self.url,
            "description": self.description,
            "graded": str(self.graded),
            "priority": self.priority,
        }
        return ans

class Event(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    startdate = models.DateTimeField(auto_now=False)
    enddate = models.DateTimeField(auto_now=False)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} for {self.Class.name}. From {str(self.startdate)} to {str(self.enddate)}"

    def getinfo(self):
        ans = {
            "id": self.id,
            "class": self.Class.getinfo(),
            "name": self.name,
            "startdate": str(self.startdate),
            "enddate": str(self.enddate),
            "description": self.description,
        }
        return ans

class Org_Event(models.Model):
    name = models.CharField(max_length=256)
    startdate = models.DateTimeField(auto_now=False)
    enddate = models.DateTimeField(auto_now=False)
    description = models.TextField()
    specialschedule = models.BooleanField(default=False)
    holiday = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name}. From {str(self.startdate)} to {str(self.enddate)}"

    def getinfo(self):
        ans = {
            "id": self.id,
            "name": self.name,
            "startdate": str(self.startdate),
            "enddate": str(self.enddate),
            "description": self.description,
            "specialschedule": self.specialschedule,
            "holiday": self.holiday,
        }
        return ans

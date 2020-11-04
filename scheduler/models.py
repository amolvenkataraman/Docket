from django.db import models
from users.models import *
from map.models import *

# Create your models here.
class Day(models.Model):
    day = models.SmallIntegerField(null=False)

    def __str__(self):
        return f"Day {self.day}"
    
    def getinfo(self):
        ans = {
            "id": self.id,
            "day": self.day,
        }
        return ans

class Slot(models.Model):
    period_no = models.SmallIntegerField(null=False)
    name = models.CharField(max_length=64)
    start = models.TimeField(auto_now=False, null=False)
    end = models.TimeField(auto_now=False, null=False)
    
    def __str__(self):
        return f"{self.name} (Period {self.period_no}). From {str(self.start)} to {str(self.end)}"
    
    def getinfo(self):
        ans = {
            "id": self.id,
            "period_no": self.period_no,
            "name": self.name,
            "start": str(self.start.strftime("%H:%M")),
            "end": str(self.end.strftime("%H:%M")),
        }
        return ans

class Period(models.Model):
    day = models.ForeignKey(Day, on_delete=models.PROTECT, related_name='slot_day')
    period = models.ForeignKey(Slot, on_delete=models.PROTECT, related_name='slot_period')

    def __str__(self):
        return f"{self.period.name} on Day {self.day.day}"

    def getinfo(self):
        ans = {
            "id": self.id,
            "day": self.day.getinfo(),
            "period": self.period.getinfo(),
        }
        return ans



class Class(models.Model):
    name = models.CharField(max_length=64, unique=True)
    teacher = models.ForeignKey(DocketUser, on_delete=models.SET("DELETED_USER"), related_name='class_teacher')
    students = models.ManyToManyField(DocketUser, related_name='class_student')
    room = models.ForeignKey(Room, on_delete=models.SET("DELETED ROOM"), related_name='class_room', null=True)
    period = models.ManyToManyField(Period, related_name='class_period')
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}, Teacher: {self.teacher.username}"

    def getinfo(self):
        ans = {
            "id": self.id,
            "name": self.name,
            "teacher": self.teacher.getinfo(),
            "period": [i.getinfo() for i in self.period.all()],
            "students": [i.getinfo() for i in self.students.all()],
            "active": str(self.active),
        }

        try:
            ans["room"] = self.room.getinfo()
        except AttributeError:
            print("", end="")

        for i in self.period.all():
            ans["period"].append(i.getinfo())

        return ans

class Group(models.Model):
    name = models.CharField(max_length=64, unique=True)
    classes = models.ManyToManyField(Class, related_name='group_class')

    def __str__(self):
        return f"{self.name}"

class Invite(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    code = models.CharField(max_length=8, unique=True)
    uses = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code}, for {self.Class.name}"

    def getinfo(self):
        ans = {
            "id": self.id,
            "class": self.Class.getinfo(),
            "code": self.code,
            "uses": self.uses,
            "active": str(self.active),
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
    sync_from = models.CharField(max_length=32, null=True, default="")
    sync_id = models.CharField(max_length=128, null=True, default="")
    
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

class Whiteboard(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.SET('DELETED_CLASS'))
    date_time = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256)
    description = models.TextField()
    img = models.ImageField(upload_to='whiteboards', null=True)

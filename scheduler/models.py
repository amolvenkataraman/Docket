from django.db import models
from users.models import DocketUser

# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=64)
    teacher = models.ForeignKey(DocketUser, on_delete=models.SET("DELETED_USER"), related_name='class_teacher')
    students = models.ManyToManyField(DocketUser, related_name='class_student')

    def __str__(self):
        return f"{self.name}, Teacher: {self.teacher.username}"

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

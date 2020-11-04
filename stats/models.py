from django.db import models
from users.models import *

# Create your models here.
class ClientDevice(models.Model):
    user = models.ForeignKey(DocketUser, on_delete=models.SET("DELETED_USER"))
    ip_address = models.CharField(max_length=15, null=True)
    cpu_cores = models.IntegerField(null=True)
    cpu_type = models.CharField(max_length=16, null=True)
    memory = models.IntegerField(null=True)
    touch_points = models.IntegerField(null=True)
    total_sw = models.IntegerField(null=True)
    total_sh = models.IntegerField(null=True)
    avail_sw = models.IntegerField(null=True)
    avail_sh = models.IntegerField(null=True)
    col_depth = models.IntegerField(null=True)
    col_res = models.IntegerField(null=True)
    language =  models.CharField(max_length=64, null=True)
    os_name = models.CharField(max_length=32, null=True)
    os_version = models.CharField(max_length=16, null=True)
    browser_name = models.CharField(max_length=32, null=True)
    browser_version = models.CharField(max_length=64, null=True)
    device_model = models.CharField(max_length=32, null=True)
    device_type = models.CharField(max_length=32, null=True)
    device_vendor = models.CharField(max_length=32, null=True)
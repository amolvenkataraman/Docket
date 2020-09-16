from django.http import HttpResponse
from django.shortcuts import render
from .models import *

# Create your views here.
def store_data(request):
    client_data = request.GET
    _ = ClientDevice(user=request.user)
    _.ip_address = request.META['REMOTE_ADDR']
    _.cpu_type = client_data["cpu_type"]
    _.language = client_data["language"]
    _.os_name = client_data["os_name"]
    _.os_version = client_data["os_version"]
    _.browser_name = client_data["browser_name"]
    _.browser_version = client_data["browser_version"]
    _.device_model = client_data["device_model"]
    _.device_type = client_data["device_type"]
    _.device_vendor = client_data["device_vendor"]

    if client_data["cpu_cores"] != "undefined":
        _.cpu_cores = client_data["cpu_cores"]
    if client_data["memory"] != "undefined":
        _.memory = client_data["memory"]
    if client_data["touch_points"] != "undefined":
        _.touch_points = client_data["touch_points"]

    _.save()
    return HttpResponse("Saved")
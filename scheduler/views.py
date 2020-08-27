from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import *
from .vars import *

import datetime
import json

# Create your views here.
@login_required(login_url="login/")
def index(request):
    return render(request, 'scheduler/schedule.html', {"vars": VARS})

@login_required(login_url="login/")
def get_data(request):
    timespan = request.GET.get("timespan")
    if timespan == None:
        return HttpResponse("Timespan not provided")
    time = request.GET.get("time")
    context = {"data": {}}
    classes = request.user.class_student.all()
    context["data"]["class"] = []
    context["data"]["assignments"] = []
    context["data"]["events"] = []
    context["data"]["org_events"] = []
    for class_ in classes:
        context["data"]["class"].append(class_.getinfo())
        if timespan == "month":
            if time == None:
                assignments = Assignment.objects.filter(Class=class_, deadline__month=(datetime.datetime.now().month))
            else:
                assignments = Assignment.objects.filter(Class=class_, deadline__month=int(time) + 1)
        elif timespan == "day":
            if time == None:
                assignments = Assignment.objects.filter(Class=class_, deadline__date=datetime.datetime.now().date)
            else:
                assignments = Assignment.objects.filter(Class=class_, deadline__date=time)
        events = Event.objects.filter(Class=class_)
        org_events = Org_Event.objects.filter()
        for assignment in assignments:
            context["data"]["assignments"].append(assignment.getinfo())
        for event in events:
            context["data"]["events"].append(event.getinfo())
        for org_event in org_events:
            context["data"]["org_events"].append(org_event.getinfo())
    return JsonResponse(context)

@login_required(login_url="login/")
def add(request):
    if request.user.teacher == True:
        if request.method == 'GET':
            context = {"classes": []}
            classes = Class.objects.filter(teacher=request.user)
            for class_ in classes:
                context['classes'].append(class_.getinfo())
            return render(request, 'scheduler/add.html', context)
        else:
            req = json.loads(request.body)
            assignment = Assignment(
                Class=Class.objects.filter(id=req["class"])[0],
                name=req["name"],
                deadline=datetime.datetime.strptime(req["deadline"], '%Y-%m-%d %H:%M'),
                url=req["url"],
                description=req["description"],
                graded=req["graded"],
                priority=req["priority"],
            )
            assignment.save()
            return HttpResponse("OK")
    else:
        return HttpResponse('Only teachers are allowed to access this.<br>Please contact me if you are a teacher and want administrative access.')

@login_required(login_url="login/")
def enroll(request):
    invitecode = request.GET.get("code")
    if invitecode == None:
        return JsonResponse({"status": "error", "data": "No Invite Code provided"})
    invite = Invite.objects.filter(code=invitecode)
    if request.method == 'GET':
        try:
            class_ = invite[0].Class
            if class_ in request.user.class_student.all():
                return JsonResponse({"status": "error", "data": "You are already enrolled in this class"})
            else:
                return JsonResponse({"status": "success", "data": class_.getinfo()})
        except IndexError:
            return JsonResponse({"status": "error", "data": "Invalid Invite Code"})
    else:
        try:
            class_ = invite[0].Class
            if class_ in request.user.class_student.all():
                return JsonResponse({"status": "error", "data": "You are already enrolled in this class"})
            else:
                class_.students.add(request.user)
                return JsonResponse({"status": "success"})
        except IndexError:
            return JsonResponse({"status": "error", "data": "Invalid Invite Code"})

"""
    if request.method == 'GET':
        class_ = Class.objects.filter(id=request.GET.get('class'))[0]
        if class_ in request.user.class_student.all():
            return HttpResponse("You are already enrolled in this class")
        else:
            return render(request, 'scheduler/enroll.html', class_.getinfo())
    else:
        class_ = Class.objects.filter(id=request.GET.get('class'))[0]
        if class_ in request.user.class_student.all():
            return HttpResponse("You are already enrolled in this class")
        else:
            class_.students.add(request.user)
            messages.success(request, f'Successfully enrolled in {class_.name}.')
            return redirect('/')
"""

@login_required(login_url="login/")
def class_(request):
    if request.method == 'GET':
        if request.user.teacher == True:
            context = {"classes": []}
            for c in Class.objects.filter(teacher=request.user):
                temp = c.getinfo()
                temp['students'] = [i.getinfo() for i in c.students.all()]
                context["classes"].append(temp)
            return render(request, 'scheduler/class.html', context)
        else:
            return HttpResponse("Only teachers are allowed to access this")
    else:
        if request.user.teacher == True:
            c = Class(name=request.body.decode('utf8'))
            c.teacher = request.user
            c.save()
            c.students.add(request.user)
            return HttpResponse("OK")
        else:
            return HttpResponse("Only teachers are allowed to access this")

def stats(request):
    context = {
        "users": DocketUser.objects.count(),
        "classes": Class.objects.count(),
        "assignments": Assignment.objects.count(),
    }
    return render(request, 'scheduler/admin.html', context)
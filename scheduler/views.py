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
    time = request.GET.get("time")
    context = {"data": {}}
    classes = request.user.class_student.all()
    for class_ in classes:
        context["data"][class_.name] = {}
        context["data"][class_.name]["assignments"] = []
        context["data"][class_.name]["events"] = []
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
        for assignment in assignments:
            context["data"][class_.name]["assignments"].append(assignment.getinfo())
        for event in events:
            context["data"][class_.name]["events"].append(event.getinfo())
    return JsonResponse(context)

@login_required(login_url="login/")
def add(request):
    if request.user.teacher == True:
        if request.method == 'GET':
            context = {"classes": []}
            classes = Class.objects.filter(teacher=request.user)
            for class_ in classes:
                context['classes'].append([class_.id, class_.name])
            return render(request, 'scheduler/add.html', context)
        else:
            print(request.body)
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

@login_required(login_url="login/")
def class_(request):
    if request.method == 'GET':
        if request.user.teacher == True:
            context = {"classes": []}
            for c in Class.objects.filter(teacher=request.user):
                context["classes"].append({
                    "id": c.id,
                    "name": c.name,
                    "students": c.students.count(),
                })
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
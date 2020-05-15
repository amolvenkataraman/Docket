from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *

import datetime
import json

# Create your views here.
@login_required(login_url="login/")
def index(request):
    context = {"assignments": {}}
    classes = request.user.class_student.all()
    for class_ in classes:
        context["assignments"][class_.name] = []
        assignments = Assignment.objects.filter(Class=class_)
        for assignment in assignments:
            context["assignments"][class_.name].append(assignment.getinfo())
    return render(request, 'scheduler/schedule.html', context)

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
        return render(request, 'scheduler/enroll.html', class_.getinfo())
    else:
        #todo
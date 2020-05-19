from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect, render
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
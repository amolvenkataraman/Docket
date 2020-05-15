from django.http import HttpResponse
from django.shortcuts import render
from .models import *

import datetime
import json

# Create your views here.
def index(request):
    context = {"assignments": {}}
    classes = request.user.class_student.all()
    for class_ in classes:
        context["assignments"][class_.name] = []
        assignments = Assignment.objects.filter(Class=class_)
        for assignment in assignments:
            context["assignments"][class_.name].append(assignment.getinfo())
    return render(request, 'scheduler/schedule.html', context)

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
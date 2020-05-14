from django.http import HttpResponse
from django.shortcuts import render
from .models import *

import datetime

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

def assignment(request):
    if request.method == 'GET':
        return render(request, 'scheduler/assignment.html')
    else:
        print("hi")
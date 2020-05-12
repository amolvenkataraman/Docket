from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'scheduler/schedule.html')

def assignment(request):
    if request.method == 'GET':
        return render(request, 'scheduler/assignment.html')
    else:
        print("hi")
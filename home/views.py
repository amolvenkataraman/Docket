from django.shortcuts import render
from scheduler.models import *
from django.db.models import Q
from django.contrib.auth.decorators import login_required

import datetime

# Create your views here.
@login_required(login_url="/login")
def index(request):
    context = {"data": {}}

    starttime = datetime.datetime.now().date()
    endtime = (starttime + datetime.timedelta(days=7))

    classes = request.user.class_student.all()
    context["data"]["class"] = [i.getinfo() for i in classes]
    assignments = []
    events = []
    #current = 
    
    if len(classes) > 0:
        for class_ in classes:
            assignments += Assignment.objects.filter(Q(Class=class_) & Q(deadline__gte=starttime) & Q(deadline__lte=endtime)).order_by('deadline')
            events += Event.objects.filter(Q(Class=class_) & ((Q(startdate__gte=(starttime)) & Q(enddate__lte=(endtime))))).order_by('startdate')
    org_events = Org_Event.objects.filter((Q(startdate__gte=starttime) & Q(enddate__lte=(endtime)))).order_by('startdate')

    context["data"]["assignments"] = [i.getinfo() for i in assignments]
    context["data"]["events"] = [i.getinfo() for i in events]
    context["data"]["org_events"] = [i.getinfo() for i in org_events]
    context["data"]["days"] = [i.getinfo() for i in Day.objects.all()]
    context["data"]["slots"] = [i.getinfo() for i in Slot.objects.all()]
    context["data"]["periods"] = [i.getinfo() for i in Period.objects.all()]

    return render(request, 'home/home.html', context)
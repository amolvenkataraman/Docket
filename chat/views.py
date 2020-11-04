from django.http import HttpResponse, JsonResponse
#from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
#from django.db.models import Q
from users.models import *
from .models import *

import requests
import datetime
import json

# Create your views here.
@login_required(login_url="/login")
def chat(request):
    context = {}
    context["users"] = [i.getinfo() for i in DocketUser.objects.all()]

    return render(request, 'chat/chat.html', context)
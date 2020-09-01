from django.http import HttpResponse, JsonResponse, FileResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import *

import PIL

# Create your views here.
@login_required(login_url="login/")
def map(request):
    return render(request, 'map/map.html')

@login_required(login_url="login/")
def map_image(request):
    venue_id = request.GET.get("venue_id")
    if venue_id != None:
        venue = Venue.objects.filter(id=venue_id)[0]
        data = request.GET.get("data")
        if data == None or data == 'image':            
            return FileResponse(venue.map_image)
        elif data == 'size':
            image = PIL.Image.open(venue.map_image.path)
            width, height = image.size
            return JsonResponse({"width": width, "height": height})
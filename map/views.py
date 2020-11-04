from django.http import HttpResponse, JsonResponse, FileResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import *

import json
import PIL

# Create your views here.
@login_required(login_url="/login")
def map(request):
    context = {
        "venues": [i.getinfo() for i in Venue.objects.all()],
        "floors": [i.getinfo() for i in Floor.objects.all()],
        "stairs": [i.getinfo() for i in Stair.objects.all()],
        "elevators": [i.getinfo() for i in Elevator.objects.all()],
        "rooms": [i.getinfo() for i in Room.objects.all()],
        "entrances": [i.getinfo() for i in Entrance.objects.all()],
        "types": [i.getinfo() for i in RoomType.objects.all()],
    }

    return render(request, 'map/map.html', {"data": context})

@login_required(login_url="/login")
def map_image(request):
    venue_id = request.GET.get("venue_id")
    floor = request.GET.get("floor")
    if venue_id != None:
        venue = Venue.objects.filter(id=venue_id)[0]
        floor = Floor.objects.filter(level=floor)[0]
        floorplan = FloorPlan.objects.filter(venue=venue, floor=floor)[0]
        data = request.GET.get("data")
        if data == None or data == 'image':            
            return FileResponse(floorplan.map_image)
        elif data == 'size':
            image = PIL.Image.open(floorplan.map_image.path)
            width, height = image.size
            return JsonResponse({"width": width, "height": height})

@login_required(login_url="/login")
def add(request):
    if request.method == 'POST':
        info = json.loads(request.body)
        if info["item"] == "room":
            temp = Room(
                name = info["name"],
                venue = Venue.objects.filter(id=info["venue"])[0],
                floor = Floor.objects.filter(level=info["floor"])[0],
                Type = RoomType.objects.filter(id=info["type"])[0],
                info = info["info"],
                bllat = info["bllat"],
                bllng = info["bllng"],
                trlat = info["trlat"],
                trlng = info["trlng"],
            )

            temp.save()
            return HttpResponse("OK")

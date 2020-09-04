from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Venue)
admin.site.register(Floor)
admin.site.register(FloorPlan)
admin.site.register(Stair)
admin.site.register(Elevator)
admin.site.register(RoomType)
admin.site.register(Room)
admin.site.register(Entrance)
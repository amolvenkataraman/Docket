from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Venue)
admin.site.register(Floor)
admin.site.register(Stair)
admin.site.register(Room)
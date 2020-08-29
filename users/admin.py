from django.contrib import admin
from .models import *

# Register your models here.
class DUAdmin(admin.ModelAdmin):
    search_fields = ('id', 'username', 'email')

admin.site.register(DocketUser, DUAdmin)

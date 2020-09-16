from django.contrib import admin
from django.db import models
import django.contrib.auth.forms
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class DUAdmin(UserAdmin):
    search_fields = ('id', 'username', 'email')
    
    fieldsets = UserAdmin.fieldsets + (
        ("Other", {
            'fields': ('parent', 'teacher', 'newuser',),
        }),
    )
    #fieldsets = UserAdmin.fieldsets


admin.site.register(DocketUser, DUAdmin)

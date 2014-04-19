from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from main.models import Manager

# Register your models here.
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

admin.site.register(Manager,          ManagerAdmin)



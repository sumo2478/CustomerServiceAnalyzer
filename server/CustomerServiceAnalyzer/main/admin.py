from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from main.models import Employee, Manager, EmployeeChatList, Chat

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']

class ManagerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

class EmployeeChatAdmin(admin.ModelAdmin):
	list_display = ['employee', 'customer_name']

class ChatAdmin(admin.ModelAdmin):
	list_display = ['chat_id', 'timestamp', 'message', 'is_employee']

admin.site.register(Manager,          ManagerAdmin)
admin.site.register(Employee,         EmployeeAdmin)
admin.site.register(EmployeeChatList, EmployeeChatAdmin)
admin.site.register(Chat,             ChatAdmin)

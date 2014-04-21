from django.contrib import admin

from employee.models import Employee, EmployeeChatList
from chat.models import Chat

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']

class EmployeeChatListAdmin(admin.ModelAdmin):
    list_display = ['employee', 'customer_name', 'sentiment', 'timestamp']

admin.site.register(Employee,         EmployeeAdmin)
admin.site.register(EmployeeChatList, EmployeeChatListAdmin)

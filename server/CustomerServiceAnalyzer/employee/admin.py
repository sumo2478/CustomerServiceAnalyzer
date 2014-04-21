from django.contrib import admin

from employee.models import Employee, EmployeeChatList
from chat.models import Chat

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']

class EmployeeChatListAdmin(admin.ModelAdmin):
	search_fields =['employee__user__first_name', 'employee__user__last_name']
	list_display = ['chat_id', 'employee', 'customer_name', 'sentiment', 'timestamp']

admin.site.register(Employee,         EmployeeAdmin)
admin.site.register(EmployeeChatList, EmployeeChatListAdmin)

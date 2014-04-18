from django.contrib import admin
from chat.models import Chat

# Register your models here.

class ChatAdmin(admin.ModelAdmin):
	list_display = ['chat_id', 'timestamp', 'message', 'is_employee', 'sentiment']
	search_fields = ['chat_id']

admin.site.register(Chat, ChatAdmin)
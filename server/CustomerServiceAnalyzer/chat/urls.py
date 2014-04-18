from django.conf.urls import patterns, url
from chat import views

urlpatterns = patterns('',
        url(r'^chatroom/$', views.chat_room, name='chatroom')  
        )

from django.conf.urls import patterns, url
from chat import views

urlpatterns = patterns('',
        url(r'^employeechatroom/$', views.employee_chat_room, name='employeechatroom'),
        url(r'^customerlobby/$', views.customer_lobby, name='customerlobby'),
        url(r'^customerchatroom/$', views.customer_chat_room, name='customerchatroom')
        )

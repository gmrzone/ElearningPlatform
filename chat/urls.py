from django.urls import path
from django.http import HttpResponse
from . import views

app_name = 'chat'

urlpatterns = [
    path('chatroom/<int:course_id>/chat/', views.course_chat_room, name='chat_room'),


]



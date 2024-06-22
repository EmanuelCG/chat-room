from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name="home"),
    path('room/<int:room_id>/', views.room, name="room"),
    
]

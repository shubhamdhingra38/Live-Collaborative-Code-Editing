from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('auth/', views.room_auth, name='room_auth'),
    path('<str:room_name>/', views.room, name='room'),
]
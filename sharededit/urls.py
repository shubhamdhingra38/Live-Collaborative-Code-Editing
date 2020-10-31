from django.urls import path

from . import views

urlpatterns = [
    path('shared/<str:room_name>/', views.test, name='index'),
]
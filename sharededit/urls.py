from django.urls import path

from . import views

urlpatterns = [
    path('<str:room_name>/', views.shared_editing, name='index'),
]
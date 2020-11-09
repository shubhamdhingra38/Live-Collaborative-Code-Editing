from django.urls import path

from . import views

urlpatterns = [
    path('run/', views.run_code, name='run_code'),
    path('<str:room_name>/', views.shared_editing, name='index'),
]
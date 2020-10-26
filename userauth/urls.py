from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='index'),
    path('register/', views.register, name='index'),
]
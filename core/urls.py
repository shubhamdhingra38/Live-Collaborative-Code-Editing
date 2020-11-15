
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls')),
    path('auth/', include('userauth.urls')),
    path('code/', include('sharededit.urls')),
]

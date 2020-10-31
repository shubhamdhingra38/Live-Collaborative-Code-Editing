from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def test(request, room_name):
    print(room_name, 'was visited')
    return render(request, "shared.html", {"room_name": room_name, "user": request.user})

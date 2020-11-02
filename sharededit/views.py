from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from chat.views import is_room_occupied
from .models import ChatUser, ChatRoom, UserAndRoom

@login_required
def shared_editing(request, room_name):
    print(room_name, 'was visited')
    if not is_room_occupied(room_name): #if not occupied, ask to set a password
       return render(request, 'shared.html', {
           'room_name': room_name,
           'set_pass': True,
       }) 
    else: #else ask user to enter the password
        chat_user = ChatUser.objects.get(chat_user=request.user)
        print(chat_user)
        chat_rooms = UserAndRoom.objects.filter(chat_user=chat_user)
        print(chat_rooms)
        for room in chat_rooms:
            if str(room.chat_room) == room_name:
                #user is already authorized
                return render(request, 'shared.html',{
                    'room_name': room_name,
                    'user': request.user
                })
        #user is not authorized, ask for password
        return render(request, 'shared.html', {
            'room_name': room_name,
            'get_pass': True,
        })

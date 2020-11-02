from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sharededit.models import ChatRoom, ChatUser, UserAndRoom
from django.http import JsonResponse, HttpResponse
import json


def index(request):
    return render(request, 'index.html', {'user': request.user})



#if the room does not exist in database or it is unoccupied, then ask user for password
def is_room_occupied(room_name):
    room = ChatRoom.objects.filter(room_name=room_name)
    assert len(room) <= 1 #unique constraint
    if len(room) == 0 or len(UserAndRoom.objects.filter(chat_room=room[0])) == 0:
        return False
    return True

@login_required
def room(request, room_name):
    if not is_room_occupied(room_name): #if not occupied, ask to set a password
       return render(request, 'chatroom.html', {
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
                return render(request, 'chatroom.html',{
                    'room_name': room_name
                })
        #user is not authorized, ask for password
        return render(request, 'chatroom.html', {
            'room_name': room_name,
            'get_pass': True,
        })

@login_required
def room_auth(request):
    """
    POST: (JSON response)
        a) creating a chatroom, or modifying existing room parameters
        b) verifying password, then authorizing the user to participate in that chatroom 
    """

    if request.method == 'POST':
        print('POST request for chat auth')

        body = json.loads(request.body)
        room_name = body['room_name']
        room_pass = body['password']
        request_type = body['type']
        
        if request_type == 'set_pass':
            if len(room_pass) < 3:
                return JsonResponse(data={"msg": "Password length must be greater than 3 characters"}, status=400)
            if is_room_occupied(room_name):
                return JsonResponse(data={"msg": "Room is already occupied!"}, status=400)
            chatroom_qs = ChatRoom.objects.filter(room_name=room_name)
            chatroom = None
            if len(chatroom_qs) == 0: #does not exist in database
                #create new object
                print('creating a new room in db')
                chatroom = ChatRoom(room_name=room_name, room_password=room_pass) #don't store in raw format TODO
                chatroom.save()
            else: #already exists
                print('changing password of room, already exists in db')
                chatroom = chatroom_qs[0]
                chatroom.room_password = room_pass
            print('chatroom over here', chatroom)
            chat_user = ChatUser.objects.get(chat_user=request.user)
            chatroom.chat_users.add(chat_user)
            chatroom.save()
            return JsonResponse(data={"msg": "Successfully set the password for the room."}, status=201)

        elif request_type == 'get_pass':
            chatroom_qs = ChatRoom.objects.filter(room_name=room_name)
            chatroom = chatroom_qs[0]
            if chatroom.room_password != room_pass:
                return JsonResponse(data={"msg": "Incorrect password!"}, status=400)
            else:
                chat_user = ChatUser.objects.get(chat_user=request.user)
                chatroom.chat_users.add(chat_user) #check what happens if already exists TODO
                chatroom.save()
                return JsonResponse(data={"msg": "Validated password, authorized access to room."}, status=200)

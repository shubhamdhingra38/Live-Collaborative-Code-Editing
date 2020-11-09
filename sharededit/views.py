from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from chat.views import is_room_occupied
from .models import ChatUser, ChatRoom, UserAndRoom
import requests
from django.views.decorators.csrf import csrf_exempt
import json
import time

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



api = {
    'sendCodeURL': 'https://ide.geeksforgeeks.org/main.php',
    'receiveResultsURL': 'https://ide.geeksforgeeks.org/submissionResult.php'
}



#TODO remove csrf exempt, make non blocking calls
@csrf_exempt
def run_code(request):
    if request.method == 'POST':
        body = {
            'lang': "Python3",
            'code': request.POST['code'],
            # 'code': code,
            'save': "false",
            'input': ""
        }
        response = requests.post(api['sendCodeURL'], body)
        res = response.json()
        print(res)
        if response.ok and 'sid' in res:
            print("ok, got results code")
            s_id = res['sid']
            time.sleep(10)
            response = requests.post(api['receiveResultsURL'], {
                'requestType': 'fetchResults',
                'sid': s_id
            })
            res = response.json()
            print(response.content)
            print(response.ok)

            if response.ok and 'valid' in res:
                valid_status = res['valid']
                if valid_status == '1':
                    #runs
                    return JsonResponse({"msg": "Ran successfully", "data": res}, status=200)
                else:
                    #some error
                    return JsonResponse({"msg": "Compilation/runtime error"}, status=400)
            # return JsonResponse({"msg": "Ok"}, status=200)
            else:
                return JsonResponse({"msg": "Failed"}, status=400)
        else:
            return JsonResponse({"msg": "Failed"}, status=400)


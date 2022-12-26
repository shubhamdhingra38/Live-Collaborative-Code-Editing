from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from chat.views import is_room_occupied
from .models import ChatUser, UserAndRoom
import requests
from django.views.decorators.csrf import csrf_exempt
import json
import time
import logging
import os


CODE_EVALUATION_URL = u'https://api.hackerearth.com/v4/partner/code-evaluation/submissions/'
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
MAX_TIME_LIMIT = 5


logger = logging.getLogger(__name__)


@login_required
def shared_editing(request, room_name):
    logger.info(f'Room {room_name} was visited')
    if not is_room_occupied(room_name):  # if not occupied, ask to set a password
        return render(request, 'shared.html', {
            'room_name': room_name,
            'set_pass': True,
        })
    else:  # else ask user to enter the password
        chat_user = ChatUser.objects.get(chat_user=request.user)
        chat_rooms = UserAndRoom.objects.filter(chat_user=chat_user)
        for room in chat_rooms:
            if str(room.chat_room) == room_name:
                # user is already authorized
                return render(request, 'shared.html', {
                    'room_name': room_name,
                    'user': request.user
                })
        # user is not authorized, ask for password
        return render(request, 'shared.html', {
            'room_name': room_name,
            'get_pass': True,
        })


# NOTE: This is very unsafe way of executing untrusted scripts. It will run the script without any sandbox environment bare bone on your machine
# If you cannot register for HackerEarth API for some reason and just want to test it on your machine, you can use this instead
# DO NOT run any commands which can affect your system

# out = StringIO()
# sys.stdout = out
# try:
#     exec(code)
#     results = out.getvalue()
#     return JsonResponse({"code": 0, "msg": "Successfully ran code", "results": results}, status=200)
# except:
#     return JsonResponse({"code": 1, "msg": "Could not execute the code"}, status=400)


@csrf_exempt
def run_code(request):
    """
    Uses HackerEarth V4 API for remote code execution
    Register here: https://www.hackerearth.com/docs/wiki/developers/v4/
    """
    if request.method == 'POST':
        body = json.loads(request.body)
        code = body['code']
        data = {
            'source': code,
            'lang': "PYTHON3",
            'time_limit': MAX_TIME_LIMIT,
            'memory_limit': 262144,
        }
        response = requests.post(CODE_EVALUATION_URL, data=data, headers={
                                 "client-secret": CLIENT_SECRET})
        response_data = response.json()
        results = response_data['result']['run_status']
        status_update_url = response_data['status_update_url']

        # TODO: Very bad way for polling status! API got changed to be async, so a temp fix for now
        # It would block the worker thread for entire duration
        while results['status'] == 'NA':
            time.sleep(MAX_TIME_LIMIT)
            response = requests.get(status_update_url, headers={
                                    "client-secret": CLIENT_SECRET})
            results = response.json()['result']['run_status']

        if results['status'] == 'AC':
            s3_url = results['output']
            execution_result = requests.get(s3_url)
            return JsonResponse({"code": 0, "msg": "Successfully ran code", "results": execution_result.text}, status=200)
        elif results['status'] == 'CE':
            return JsonResponse({"code": 2, "msg": "Compilation error"}, status=200)
        elif results['status'] == 'RE':
            return JsonResponse({"code": 1, "msg": "Could not execute the code", "results": results['stderr']}, status=200)
        else:
            return JsonResponse({"code": -1, "msg": "Unexpected error"}, status=400)

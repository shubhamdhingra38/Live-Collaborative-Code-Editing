from django.apps import AppConfig
# import django
# django.setup()
# from sharededit.models import ChatUser, ChatRoom, UserAndRoom

class ChatConfig(AppConfig):
    name = 'chat'
    # def ready(self): #run once per startup of server
    #     print("Server restarted, dropping all existing chat room from database\n" * 10)
    #     print(len(UserAndRoom.objects.all()))
    #     UserAndRoom.objects.all().delete()
    #     print(len(UserAndRoom.objects.all()))



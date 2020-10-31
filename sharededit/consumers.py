import json
from channels.generic.websocket import AsyncWebsocketConsumer


class SharedEditConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print("received exit from user", self.user.username)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'disconnect_message',
                'message': f'{self.user.username} has left.'
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )



    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        cursor_pos = text_data_json['cursor']
        text = text_data_json['text']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'text_change',
                'text': text,
                'username': self.user.username,
                'cursor_pos': cursor_pos,
            }
        )

    async def text_change(self, event):
        text = event['text']
        username = event['username']
        print("got some text", text)
        cursor_pos = event['cursor_pos']
        print("cursor position is", cursor_pos)

        await self.send(text_data=json.dumps({
            'text': text,
            'username': username,
        }))

    async def disconnect_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
    
    async def connect_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    pass

import json
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone


# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         self.send(text_data=json.dumps({
#             'message': message
#         }))



# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.id = self.scope['url_route']['kwargs']['course_id']
#         self.user = self.scope['user']
#         self.room_group_name = f'chat_{self.id}'
#         async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
#         self.accept()

#     def disconnect(self, code):
#         async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
#         now = timezone.now()
#         async_to_sync(self.channel_layer.group_send)(self.room_group_name, {'type': 'chat_message', 'message': message, 'time': now.isoformat(), 'username': self.user.username})

#     def chat_message(self, event):
#         self.send(text_data=json.dumps(event))


# Async Consumer
class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f"chat_{self.id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'chat_message',
            'message': message,
            'username': self.user.username,
            'time': now.isoformat()
        })
        
    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))
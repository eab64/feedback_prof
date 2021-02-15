# chat/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message, Chats, ChatUser
from django.contrib.auth import get_user_model

User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):#Берет последний 10 сообщений и пересылает по сути в тот же чат
        print('fetch function started')
        print(data)
        # chat_id = data['chat_id']
        messages = Message.last_10_messages()
        content = {
            'command':'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)
        print('fetch function end')

    def new_message(self, data):#Откуда идет дата, с JS?
        print(data)
        print(data)
        author = data["from"]#Это он берет User_id
        author_user = User.objects.filter(username=author)[0]#По user_id находит автора
        # chat_id = data['chat']
        message = Message.objects.create(
            author = author_user,
            content = data['message'],
            # chat = chat_id#При созданий сообщения, на верху создался чат
            )
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def connect(self):
        print('-----------------CONNECTED SUCCESFULLY------------')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print('------------CONNECTION CLOSED---------------------')

    def receive(self, text_data):#Принимает сообщения
        print('------------------RECEIVED---------------------------')
        data = json.loads(text_data)
        self.commands[data['command']](self, data)


    def send_chat_message(self, message):
        print('------------------SENDING MESSAGE TO CHAT-------------')
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )

    def send_message(self, message):
        print('333333333333333333333333333333333333333333333333')
        print(message)
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        print(type(event))#{'type': 'chat_message', 'message': {'command': 'new_message', 'message': {'author': 'yeldos', 'content': 'testtt', 'timestamp': '2021-01-28 05:38:37.603678+00:00'}}}
        message = event['message']
        a = json.dumps(message)
        print(message)
        self.send(text_data=json.dumps(event['message']))
        print('444444444444444444444444444444444444444444444444')


    def messages_to_json(self, messages):#
        print('555555555555555555555555555555555555555555555555555')
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        print('------------------MESSAGE TO JSON-------------------')
        return {
        'author': message.author.username,
        'content': message.content,
        'timestamp': str(message.timestamp),
        # 'chat': message.chat
        }
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

# chat/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Max
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import datetime
from .models import Chats, ChatUser, Message
from .serializers import ChatsSerializer, UserSerializer
from django.core.paginator import Paginator
import requests


# Userr = get_user_model()

# def index(request):
#     return render(request, 'chat/index.html', {})
#
# @login_required
# def room(request, room_name):
#     return render(request, 'chat/room.html', {
#         'room_name_json': mark_safe(json.dumps(room_name)),
#         'username': mark_safe(json.dumps(request.user.username)),# Вместо этого берем user_id
#         # 'chat': room_name добавил тут
#     })



# def enter_room(request, chat_id=1):
#     '''Когда будет база примет user_id и найдет через нее chat_id'''


# CHAT
# @api_view(['GET'])
def main(request, user_id):
    try:
        chatUser = ChatUser.objects.get(user_id=user_id)#Смотрим есть ли чат с таким user_id
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps('SmartPlaza Chat')),
            # 'username': mark_safe(json.dumps(request.user.username)),
            'chat_id': mark_safe(json.dumps(chatUser.chatik.id)),
            'user_id': mark_safe(json.dumps(user_id))
        })

    except ChatUser.DoesNotExist:#Если такого Юзера нет, создаем новый чат и привязываем его к новому юзеру
        new_chat = Chats.objects.create(name='SmartPlaza Chat')
        chat_id = new_chat.id
        ChatUser.objects.create(chatik=new_chat, user_id=user_id)
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(new_chat.name)),
            # 'username': mark_safe(json.dumps(request.user.username)),
            'chat_id': mark_safe(json.dumps(new_chat.id)),
            'user_id': mark_safe(json.dumps(user_id))
        })


def sign_in(request):
    return render(request, 'chat/button.html')

def last_messages(request):
    list = []
    queryset = Message.objects.order_by('-timestamp').filter(chat_id = 2)
    chats = Chats.objects.all().values_list('id', flat=True)
    for message in queryset:
        list.append(message.content)

    return render(request, 'chat/admin.html', {'messages': chats[0]})


class ChatsView(viewsets.ModelViewSet):
    queryset = Chats.objects.all()
    serializer_class = ChatsSerializer

'''Выдает всех Юзеров с базы'''
class UserView(viewsets.ModelViewSet):
    queryset = ChatUser.objects.all()
    serializer_class = UserSerializer




# dict = {
#            id: 123,
#            users:user:1,
#            message:[userName: name, message: "text",
#             createdAt: "2021-02-20 12:13:10"],
#                     [userName: name, message: "text", createdAt: "2021-02-20 12:13:10"] },
#          }
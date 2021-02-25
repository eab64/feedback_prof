# chat/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Max
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from rest_framework import viewsets, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
import json
import datetime
from .models import Chats, ChatUser, Message
from .serializers import ChatsSerializer, UserSerializer, MessageSerializer
from django.core.paginator import Paginator
import requests



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


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def last_messages(request):
    user_list = Message.objects.all()
    # a = list(x)
    # for i in a:
    #     user_list.append(Message.objects.filter(chat_id=i).latest('timestamp'))
    page = request.GET.get('page', 1)
    paginator = Paginator(user_list, 10)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    return render(request, 'chat/admin.html', { 'users': users })

class MessagesView(APIView):
    """Last messages by pagination"""
    def get(self, request):
        messages_list = []
        last_mess_indexes = Message.objects.all().values_list('chat_id', flat=True).distinct()
        indexes = list(last_mess_indexes)
        for i in indexes:
            messages_list.append(Message.objects.filter(chat_id=i).latest('timestamp'))

        paginator = Paginator(messages_list, 10)
        page = request.GET.get('page')
        try:
            messages_list = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            messages_list = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            messages_list = paginator.page(paginator.num_pages)
        serializer = MessageSerializer(messages_list, many=True)
        return Response({'messages': serializer.data})



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
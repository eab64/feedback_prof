# chat/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Max
from django.db.models import Q
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from rest_framework import viewsets, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework import viewsets, status


import json
import datetime
from .models import Chats, ChatUser, Message
from .serializers import ChatsSerializer, UserSerializer, MessageSerializer, MFSerializer, ChatUserSerializer
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

@api_view(['GET'])
def index(request, user_id):#Что передается в room.html всегда?
    try:
        chatUser = ChatUser.objects.get(user_id=user_id)
        render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps('SmartPlaza Chat')),
            'username': mark_safe(json.dumps(user_id)),
            'chat_id': mark_safe(json.dumps(chatUser.chatik.id))})
        result = chatUser.chatik.id

    except ChatUser.DoesNotExist:
        new_chat = Chats.objects.create(name='SmartPlaza Chat')
        chat_id = new_chat.id
        ChatUser.objects.create(chatik=new_chat, user_id=user_id)
        ChatUser.objects.create(chatik=new_chat, user_id=1)
        ChatUser.objects.create(chatik=new_chat, user_id=12)
        Message.objects.create(content='Здравствуйте вас привествует SmartPlaza! Чем можем вам помочь?',
                               chat_id=chat_id,
                               author=12, timestamp=datetime.now(), is_solved=True)
        render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(new_chat.name)),
            'username': mark_safe(json.dumps(user_id)),
            'chat_id': mark_safe(json.dumps(chat_id))
        })
        result = chat_id

    return Response({
        'chat_id': result,

    })


@api_view(['GET'])
def enter_chat(request):
    user_id = request.query_params.get('user_id')

    try:
        chatUser = ChatUser.objects.get(user_id=user_id)
        result = chatUser.chatik.id

    except ChatUser.DoesNotExist:
        new_chat = Chats.objects.create(name='SmartPlaza Chat')
        chat_id = new_chat.id
        ChatUser.objects.create(chatik=new_chat, user_id=user_id)
        # ChatUser.objects.create(chatik=new_chat, user_id=1)
        # ChatUser.objects.create(chatik=new_chat, user_id=12)
        result = chat_id

    return Response({
        'chat_id': result,
    })

def sign_in(request):
    user_id= request.query_params.get('user_id')
    return render(request, 'chat/button.html')


@api_view(['GET'])
@permission_classes((AllowAny,))
def paginated_messages(request):
    Message.objects.filter(chat_id=request.query_params.get('chat_id')).update(is_read=True)
    try:
        pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
        paginator = pagination_class()
        messages = Message.objects.filter(chat_id=request.query_params.get('chat_id')).order_by('-id').all()

        page = paginator.paginate_queryset(messages, request)
        serializer = MFSerializer(page, many=True)
        for n_message in serializer.data:
            n_message['timestamp'] = n_message['timestamp'].replace("T", " ").replace("Z", "")

        result = paginator.get_paginated_response(reversed(serializer.data))
        (result.data).update({'user': 'Yeldos'})

    except ChatUser.DoesNotExist:
        result = Response(status=status.HTTP_400_BAD_REQUEST)

    return result


@api_view(['GET'])
def last_messages(request):
    get_data = request.query_params
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS
    paginator = pagination_class()

    if 'sortBy' in get_data:
        sortBy = get_data['sortBy']
    else:
        sortBy = '-timestamp'

    if 'user_id' in get_data:

        chatUser = ChatUser.objects.filter(user_id=get_data['user_id']).first()
        serializer = ChatUserSerializer(chatUser)
        user = serializer.data
        chat_id = user['chatik_id']

        chat = Q(chat_id=chat_id)
    else:

        chat = Q(chat_id__isnull=False)

    if 'is_read' in get_data:

        is_read = Q(is_read=get_data['is_read'])
    else:

        is_read = Q(is_read__isnull=False)


    queryset = Message.objects.values('chat_id').annotate(pk=Max('id')).all()

    messageIds = list()

    for n in queryset:
        messageIds.append(n['pk'])
    messages = Message.objects.filter(pk__in=messageIds).filter(is_read ,chat).order_by(
        sortBy)

    page = paginator.paginate_queryset(messages, request)
    serializer = MFSerializer(page, many=True)

    result = paginator.get_paginated_response(serializer.data)

    return result


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
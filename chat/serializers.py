from .models import ChatUser, Chats, Message

from rest_framework import serializers

class MessageSerializer(serializers.Serializer):
    content = serializers.CharField()
    timestamp = serializers.DateTimeField()
    chat = serializers.CharField()



class ChatsSerializer(serializers.HyperlinkedModelSerializer):
    """"""
    class Meta:
        model = Chats
        fields = ('id', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """"""
    class Meta:
        model = ChatUser
        fields = ('id', 'user_id', 'chatik')
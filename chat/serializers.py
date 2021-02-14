from .models import ChatUser, Chats

from rest_framework import serializers

class MessageSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()


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
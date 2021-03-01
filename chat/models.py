from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Chats(models.Model):
    name = models.CharField(max_length=50)


class Message(models.Model):
    # author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chats, related_name='chat', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    def __str__(self):
        return self.content

    def last_10_messages(chat_id):
        # return Message.objects.order_by('timestamp').all()[:]
        return Message.objects.filter(chat=chat_id).order_by('timestamp').all()


class ChatUser(models.Model):
    """Юзер привязанный к чатам через ОДИНкМНОГИМ"""
    user_id = models.BigIntegerField(default=12,null=False)
    chatik = models.ForeignKey(Chats, related_name='chatik', on_delete=models.CASCADE)


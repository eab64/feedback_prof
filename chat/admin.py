from django.contrib import admin
from .models import Message, ChatUser, Chats


admin.site.register(Message)
admin.site.register(ChatUser)
admin.site.register(Chats)

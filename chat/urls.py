from django.urls import path, include

from . import views



urlpatterns = [
    path('open/<int:user_id>', views.main),#Тестовая, рендерит html комнаты
    path('chatmessages', views.paginated_messages, name='ПО чат айди возвращает все сообщения'),
    path('last/messages/', views.last_messages, name='Все последние сообщения из всех чатов'),
    path('create/or/open', views.enter_chat, name='Enter to chat'),
]



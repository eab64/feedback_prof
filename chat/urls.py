from django.urls import path, include

from . import views
from .views import MessagesView


urlpatterns = [
    # path('', views.index, name='index'),
    # path('<str:room_name>/', views.room, name='room'),
    path('open/<int:user_id>', views.main),
    path('go_room', views.sign_in),
    path('adminka', views.last_messages),
    path('last', MessagesView.as_view())
]



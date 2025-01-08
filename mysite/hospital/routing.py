from django.urls import path
from .cunsumers import *

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/',ChatConsumer.as_asgi()),
]


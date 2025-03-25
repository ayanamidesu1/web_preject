from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/chat/', consumers.ChatConsumer.as_asgi()),
]
# 启动命令daphne -b 0.0.0.0 -p 2233 djangoWebServer.asgi:application

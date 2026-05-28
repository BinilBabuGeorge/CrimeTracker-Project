from django.urls import re_path
from ctapp import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_id>\d+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/panic/admin/$', consumers.PanicConsumer.as_asgi()),
    re_path(r'ws/panic/station/(?P<station_id>\d+)/$', consumers.PanicConsumer.as_asgi()),
]

"""
This file is for routing to the consumer
"""

from django.urls import path, re_path

from .consumers import MainConsumer

websocket_urlpatterns = [
    re_path(r"ws/ride-share/$", MainConsumer.as_asgi()),
]

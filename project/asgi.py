"""
ASGI config for project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
from django.urls import path
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from smart_meter_api.consumers import MyMqttConsumer, MyWsConsumer

# from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

application = get_asgi_application()

websocket_url_pattern = [
    path("ws/dashboard/", MyWsConsumer.as_asgi()),
]

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "mqtt": MyMqttConsumer.as_asgi(),
        "websocket": AuthMiddlewareStack(URLRouter(websocket_url_pattern)),
    }
)

# TODO: Validate origin of websocket requests AllowedHostsOriginValidator(),

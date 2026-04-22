"""
ASGI config for capstone project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
import socketio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'capstone.settings')
django_app = get_asgi_application()

from chat.socketio_events import sio

application = socketio.ASGIApp(sio, django_app)
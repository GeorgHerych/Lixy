"""
ASGI config for Lixy project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Lixy.settings')

django_asgi_app = get_asgi_application()

try:
    from members import routing as members_routing
except Exception:  # pragma: no cover - fallback when apps not ready
    members_routing = None

websocket_router = URLRouter(members_routing.websocket_urlpatterns) if members_routing else URLRouter([])

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(websocket_router),
    }
)

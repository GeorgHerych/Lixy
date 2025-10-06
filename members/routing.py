from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/dialogs/<str:username>/', consumers.DialogConsumer.as_asgi(), name='dialog_ws'),
]

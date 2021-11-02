from django.urls import path

from .consumers import ObjectTrackingConsumer

ws_urlpatterns = [
    path('ws/tracking', ObjectTrackingConsumer.as_asgi()),
]
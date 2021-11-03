from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

class TrackingMixin:
    object_name = None
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if self.request.method in ('POST', 'PATCH', 'PUT', 'DELETE') and 200 <= response.status_code <= 299:
            async_to_sync(channel_layer.group_send)('tracking_channel', {
                'type': 'send_message', 
                'payload': {
                    'tracking_object': str(self.__class__.object_name)
                }
            })
        return response
    
    

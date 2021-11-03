import json

from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ObjectTrackingConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.message_group_name = 'tracking_channel'
        await self.channel_layer.group_add(self.message_group_name, self.channel_name)
        await self.accept()
            
    async def send_message(self, res):
        await self.send(text_data=json.dumps(res['payload']))    
        
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.message_group_name, self.channel_name)
        
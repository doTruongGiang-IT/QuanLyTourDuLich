import asyncio
import json

import websockets
from BUS.tour import (LocationBUS, TourBUS, TourCharacteristicBUS,
                      TourPriceBUS, TourTypeBUS)

SOCKER_URL = 'ws://localhost:8000/ws/tracking'

CLASS_TO_OBJECT_NAMES = {
    'tour': TourBUS,
    'tour_characteristic': TourCharacteristicBUS,
    'tour_type': TourTypeBUS,
    'tour_price': TourPriceBUS,
    'location': LocationBUS
}

async def lazy_loading():
    async with websockets.connect(SOCKER_URL) as websocket:
        while True:
            msg = await websocket.recv()
            msg = json.loads(msg)
            
            if 'tracking_object' in msg and msg['tracking_object'] in CLASS_TO_OBJECT_NAMES:
                CLASS_TO_OBJECT_NAMES[msg['tracking_object']].TRACKING_STATUS = False
                print(msg['tracking_object'])

def async_lazy_loading():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(lazy_loading())
    loop.close()
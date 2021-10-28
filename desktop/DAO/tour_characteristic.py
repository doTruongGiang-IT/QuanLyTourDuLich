import requests
from desktop.DAO.base import API_URL
from desktop.DTO.tour import TourCharacteristic


class TourCharacteristicDAO():
    TOUR_API_URL = f'{API_URL}/tour/tour_characteristic'
    
    def read(self) -> tuple[str, list[TourCharacteristic]]:
        request = requests.get(self.TOUR_API_URL)
    
        if request.status_code == 200:
            response = request.json()
            result = []
            
            for data in response['results']:
                result = TourCharacteristic(**data)
                
            return ('', result)
        else:
            return ('Get the tour characteristic list that have an error', None)
    
    def create(self, data: TourCharacteristic) -> str:
        request_data = {
            'id': data.id,
            'name': data.name
        }
        
        request = requests.post(self.TOUR_API_URL, data=request_data)
        
        if request.status_code == 201:
            return ''
        else:
            return 'create new tour characteristic that have an error'
        
    def update(self, data: TourCharacteristic) -> str:
        tour_id = TourCharacteristic.id
        request_data = {
            'id': data.id,
            'name': data.name,
            'characteristic': data.characteristic.id,
            'type': data.type.id,
            'price': data.price.id,
            'location': data.location.id
        }
        
        request = requests.patch(f'{self.TOUR_API_URL}/{tour_id}', data=request_data)
        
        if request.status_code == 200:
            return ''
        else:
            return 'update a tour characteristic that have an error'
        
    def delete(self, tour_characteristic_id: int) -> str:
        request = requests.delete(f'{self.TOUR_API_URL}/{tour_characteristic_id}')
        
        if request.status_code == 204:
            return ''
        else:
            return 'delete a tour characteristic that have an error'
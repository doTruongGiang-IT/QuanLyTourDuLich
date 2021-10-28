import requests
from desktop.DAO.base import API_URL
from desktop.DTO.tour import Tour


class TourDAO():
    TOUR_API_URL = f'{API_URL}/tour'
    
    def read(self) -> tuple[str, list[Tour]]:
        request = requests.get(self.TOUR_API_URL)
    
        if request.status_code == 200:
            response = request.json()
            result = []
            
            for data in response['results']:
                result = Tour(**data)
                
            return ('', result)
        else:
            return ('Get the tour list that have an error', None)
    
    def create(self, data: Tour) -> str:
        request_data = {
            'id': data.id,
            'name': data.name,
            'characteristic': data.characteristic.id,
            'type': data.type.id,
            'price': data.price.id,
            'location': data.location.id
        }
        
        request = requests.post(self.TOUR_API_URL, data=request_data)
        
        if request.status_code == 201:
            return ''
        else:
            return 'create new tour that have an error'
        
    def update(self, data: Tour) -> str:
        tour_id = Tour.id
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
            return 'update a tour that have an error'
        
    def delete(self, tour_id: int) -> str:
        request = requests.delete(f'{self.TOUR_API_URL}/{tour_id}')
        
        if request.status_code == 204:
            return ''
        else:
            return 'delete a tour that have an error'
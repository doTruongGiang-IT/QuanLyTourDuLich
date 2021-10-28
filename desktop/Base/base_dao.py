import requests


class BaseDAO():
    DTO_CLASS = None
    API_URL = {
        'read': '',
        'read_detail': '',
        'create': '',
        'update': '',
        'delete': ''
    }
    
    def to_create_request_data(self, data: DTO_CLASS) -> dict:
        pass
    
    def to_update_request_data(self, data: DTO_CLASS) -> dict:
        request_data = self.to_create_request_data(data)
        request_data['id'] = data.id
        return request_data
    
    def get_object(self, data: dict):
        return self.DTO_CLASS(**data)
    
    def read(self) -> tuple[str, list[DTO_CLASS]]:
        request = requests.get(self.API_URL['read'])
    
        if request.status_code == 200:
            response = request.json()
            result = []
            
            for data in response['results']:
                result.append(self.get_object(data))
                
            return ('', result)
        else:
            return ('Get the tour list that have an error', None)
    
    def read_detail(self, tour_id: int) -> tuple[str, DTO_CLASS]:
        request = requests.get(self.API_URL['read_detail'].format(tour_id))
    
        if request.status_code == 200:
            response = request.json()
            result = self.get_object(response)
                
            return ('', result)
        else:
            return ('Get the tour that have an error', None)
    
    def create(self, data: DTO_CLASS) -> str:
        request_data = self.to_create_request_data(data)
        request = requests.post(self.API_URL['create'], data=request_data)
        
        if request.status_code == 201:
            return ''
        else:
            return 'create new tour that have an error'
        
    def update(self, data: DTO_CLASS) -> str:
        request_data = self.to_update_request_data(data)
        request = requests.patch(self.API_URL['update'].format(data.id), data=request_data)
        
        if request.status_code == 200:
            return ''
        else:
            return 'update a tour that have an error'
        
    def delete(self, tour_id: int) -> str:
        request = requests.delete(self.API_URL['delete'].format(tour_id))
        
        if request.status_code == 204:
            return ''
        else:
            return 'delete a tour that have an error'
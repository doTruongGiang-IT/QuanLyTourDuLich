import requests
from Base.error import Error


API_HOST = 'http://localhost:8000'
BASE_API_URL = f'{API_HOST}/api'


class BaseDAO:
    DTO_CLASS = None
    API_URL = {
        'read': '',
        'read_detail': '',
        'create': '',
        'update': '',
        'delete': ''
    }
    
    def to_create_request_data(self, data: DTO_CLASS) -> dict:
        """
        Convert DTO_CLASS to request's data when using post method
        This method need to be overrided
        :data: DTO_CLASS -> DTO_CLASS instance
        :return: dict -> request's data
        """
        pass
    
    def to_update_request_data(self, data: DTO_CLASS) -> dict:
        """
        Convert DTO_CLASS to request's data when using post method
        :data: DTO_CLASS -> DTO_CLASS instance
        :return: dict -> request's data
        """
        request_data = self.to_create_request_data(data)
        request_data['id'] = data.id
        return request_data
    
    def get_object(self, data: dict) -> DTO_CLASS:
        """
        Convert data to DTO_CLASS instance
        :data: dict
        :return: DTO_CLASS
        """
        return self.DTO_CLASS(**data)
    
    def read(self) -> tuple[Error, list[DTO_CLASS]]:
        """
        Read method in DAO, equivalent to GET method (get list action)
        :return: tuple[Error, list[DTO_CLASS]]
        """
        request = requests.get(self.API_URL['read'])
    
        if request.status_code == 200:
            response = request.json()
            result = []
            
            for data in response['results']:
                result.append(self.get_object(data))
                
            return (Error(False, None), result)
        else:
            return (Error(True, 'Get the tour list that have an error'), None)
    
    def read_detail(self, tour_id: int) -> tuple[Error, DTO_CLASS]:
        """
        Read detail method in DAO, equivalent to GET method (get detail action)
        :tour_id: int -> Tour id
        :return: tuple[Error, DTO_CLASS]
        """
        request = requests.get(self.API_URL['read_detail'].format(tour_id))
    
        if request.status_code == 200:
            response = request.json()
            result = self.get_object(response)
                
            return (Error(False, None), result)
        else:
            return (Error(True, 'Get the tour that have an error'), None)
    
    def create(self, data: DTO_CLASS) -> Error:
        """
        Create method in DAO, equivalent to POST method (create action)
        :data: DTO_CLASS -> DTO_CLASS instance
        :return: Error
        """
        request_data = self.to_create_request_data(data)
        request = requests.post(self.API_URL['create'], data=request_data)
        
        if request.status_code == 201:
            return Error(False, None)
        else:
            return Error(True, 'create new tour that have an error')
        
    def update(self, data: DTO_CLASS) -> Error:
        """
        Update method in DAO, equivalent to PATCH method (partial_update action)
        :data: DTO_CLASS -> DTO_CLASS instance
        :return: Error
        """
        request_data = self.to_update_request_data(data)
        request = requests.patch(self.API_URL['update'].format(data.id), data=request_data)
        
        if request.status_code == 200:
            return Error(False, None)
        else:
            return Error(True, 'update a tour that have an error')
        
    def delete(self, tour_id: int) -> Error:
        """
        Delete method in DAO, equivalent to delete method (destroy action)
        :tour_id: int -> Tour id
        :return: Error
        """
        request = requests.delete(self.API_URL['delete'].format(tour_id))
        
        if request.status_code == 204:
            return Error(False, None)
        else:
            return Error(True, 'delete a tour that have an error')
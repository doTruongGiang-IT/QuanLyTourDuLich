import requests
from Base.base_dao import BaseDAO
from DAO.base import API_URL
from DTO.tour import Tour, TourCharacteristic

    
class TourCharacteristicDAO(BaseDAO):
    DTO_CLASS = TourCharacteristic
    API_URL = {
        'read':         f'{API_URL}/tour/tour_characteristic',
        'create':       f'{API_URL}/tour/tour_characteristic',
        'read_detail':  f'{API_URL}/tour/tour_characteristic',
        'update':       f'{API_URL}/tour/tour_characteristic/{{}}',
        'delete':       f'{API_URL}/tour/tour_characteristic/{{}}'
    }
    
    def to_create_request_data(self, data: DTO_CLASS) -> dict:
        request_data = {
            'name': data.name
        }
        return request_data
    
    
class TourDAO(BaseDAO):
    DTO_CLASS = Tour
    API_URL = {
        'read':         f'{API_URL}/tour',
        'create':       f'{API_URL}/tour',
        'read_detail':  f'{API_URL}/tour/{{}}',
        'update':       f'{API_URL}/tour/{{}}',
        'delete':       f'{API_URL}/tour/{{}}'
    }
    
    def get_object(self, data: dict):
        data['characteristic'] = TourCharacteristicDAO().read_detail(data['characteristic'])
        return self.DTO_CLASS(**data)
    
    def to_create_request_data(self, data: DTO_CLASS) -> dict:
        request_data = {
            'name': data.name,
            'characteristic': data.characteristic.id,
            'type': data.type.id,
            'price': data.price.id,
            'location': data.location.id
        }
        return request_data
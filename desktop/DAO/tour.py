from datetime import datetime
from Base.base_dao import BaseDAO, BASE_API_URL
from DTO.tour import Tour, TourCharacteristic, TourType, TourPrice, Location

    
class TourCharacteristicDAO(BaseDAO):
    DTO_CLASS = TourCharacteristic
    API_URL = {
        'read':         f'{BASE_API_URL}/tour/tour_characteristic',
        'create':       f'{BASE_API_URL}/tour/tour_characteristic',
        'read_detail':  f'{BASE_API_URL}/tour/tour_characteristic/{{}}',
        'update':       f'{BASE_API_URL}/tour/tour_characteristic/{{}}',
        'delete':       f'{BASE_API_URL}/tour/tour_characteristic/{{}}'
    }
    
    def to_create_request_data(self, data):
        request_data = {
            'name': data.name
        }
        return request_data
    

class TourTypeDAO(BaseDAO):
    DTO_CLASS = TourType
    API_URL = {
        'read':         f'{BASE_API_URL}/tour/tour_type',
        'create':       f'{BASE_API_URL}/tour/tour_type',
        'read_detail':  f'{BASE_API_URL}/tour/tour_type/{{}}',
        'update':       f'{BASE_API_URL}/tour/tour_type/{{}}',
        'delete':       f'{BASE_API_URL}/tour/tour_type/{{}}'
    }
    
    def to_create_request_data(self, data):
        request_data = {
            'name': data.name
        }
        return request_data
    
    
class TourPriceDAO(BaseDAO):
    DTO_CLASS = TourPrice
    API_URL = {
        'read':         f'{BASE_API_URL}/tour/tour_price',
        'create':       f'{BASE_API_URL}/tour/tour_price',
        'read_detail':  f'{BASE_API_URL}/tour/tour_price/{{}}',
        'update':       f'{BASE_API_URL}/tour/tour_price/{{}}',
        'delete':       f'{BASE_API_URL}/tour/tour_price/{{}}'
    }
    
    def get_object(self, data):
        data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%d')
        data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%d')
        return self.DTO_CLASS(**data)
    
    def to_create_request_data(self, data):
        request_data = {
            'name': data.name,
            'price': data.price,
            'start_date': data.start_date.strftime("%Y-%m-%d"),
            'end_date': data.end_date.strftime("%Y-%m-%d")
        }
        return request_data
    

class LocationDAO(BaseDAO):
    DTO_CLASS = Location
    API_URL = {
        'read':         f'{BASE_API_URL}/tour/location',
        'create':       f'{BASE_API_URL}/tour/location',
        'read_detail':  f'{BASE_API_URL}/tour/location/{{}}',
        'update':       f'{BASE_API_URL}/tour/location/{{}}',
        'delete':       f'{BASE_API_URL}/tour/location/{{}}'
    }
    
    def to_create_request_data(self, data: Location) -> dict:
        request_data = {
            'name': data.name,
            'type': data.type,
            'level': data.level
        }
        return request_data
    
    
class TourDAO(BaseDAO):
    DTO_CLASS = Tour
    API_URL = {
        'read':         f'{BASE_API_URL}/tour',
        'create':       f'{BASE_API_URL}/tour/',
        'read_detail':  f'{BASE_API_URL}/tour/{{}}',
        'update':       f'{BASE_API_URL}/tour/{{}}',
        'delete':       f'{BASE_API_URL}/tour/{{}}'
    }
    tour_characteristic_dao = TourCharacteristicDAO()
    tour_type_dao = TourTypeDAO()
    tour_price_dao = TourPriceDAO()
    location_dao = LocationDAO()
    
    def get_object(self, data):
        _, data['characteristic'] = self.tour_characteristic_dao.read_detail(data['characteristic'])
        _, data['type'] = self.tour_type_dao.read_detail(data['type'])
        _, data['price'] = self.tour_price_dao.read_detail(data['price'])
        _, data['location'] = self.location_dao.read_detail(data['location'])
        print(data['location'])
        return self.DTO_CLASS(**data)
    
    def to_create_request_data(self, data):
        request_data = {
            'name': data.name,
            'description': data.description,
            'characteristic': data.characteristic.id,
            'type': data.type.id,
            'price': data.price.id,
            'location': data.location.id
        }
        return request_data
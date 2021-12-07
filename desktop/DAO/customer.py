from Base.base_dao import BASE_API_URL, BaseDAO
from DTO.customer import Customer
from DAO.tour import LocationDAO

class CustomerDAO(BaseDAO):
    DTO_CLASS = Customer
    API_URL = {
        'read':         f'{BASE_API_URL}/customer',
        'create':       f'{BASE_API_URL}/customer',
        'read_detail':  f'{BASE_API_URL}/customer/{{}}',
        'update':       f'{BASE_API_URL}/customer/{{}}',
        'delete':       f'{BASE_API_URL}/customer/{{}}'
    }
    location_dao = LocationDAO()
    
    def to_create_request_data(self, data):
        request_data = {
            'name': data.name,
            'id_number': data.id_number,
            'address': data.address,
            'gender': data.gender,
            'phone_number': data.phone_number
        }
        return request_data
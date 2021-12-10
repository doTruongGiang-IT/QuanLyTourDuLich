from Base.base_dao import BASE_API_URL, BaseDAO
from DTO.customer import Customer, GroupCustomer
from Base.error import Error
import requests

class CustomerDAO(BaseDAO):
    DTO_CLASS = Customer
    API_URL = {
        'read':         f'{BASE_API_URL}/customer',
        'create':       f'{BASE_API_URL}/customer/',
        'read_detail':  f'{BASE_API_URL}/customer/{{}}',
        'update':       f'{BASE_API_URL}/customer/{{}}',
        'delete':       f'{BASE_API_URL}/customer/{{}}'
    }
    
    def to_create_request_data(self, data):
        request_data = {
            'name': data.name,
            'id_number': data.id_number,
            'address': data.address,
            'gender': data.gender,
            'phone_number': data.phone_number
        }
        return request_data

class GroupCustomerDAO(BaseDAO):
    DTO_CLASS = GroupCustomer
    API_URL = {
        'read':         f'{BASE_API_URL}/customer/group/{{}}',
        'create':       f'{BASE_API_URL}/customer/group/',
        'read_detail':  f'{BASE_API_URL}/customer/group/{{}}',
        'update':       f'{BASE_API_URL}/customer/group/{{}}',
        'delete':       f'{BASE_API_URL}/customer/group/{{}}'
    }

    def read(self, group_id) -> tuple[Error, list[DTO_CLASS]]:
        """
        Read method in DAO, equivalent to GET method (get list action)
        :return: tuple[Error, list[DTO_CLASS]]
        """
        request = requests.get(self.API_URL['read'].format(group_id))
    
        if request.status_code == 200:
            response = request.json()
            result = []
            
            for data in response:
                result.append(self.get_object(data))
                
            return (Error(False, None), result)
        else:
            return (Error(True, 'Get the tour list that have an error'), None)

    def delete(self, group_id: int, customer_id) -> Error:
        """
        Delete method in DAO, equivalent to delete method (destroy action)
        :tour_id: int -> Tour id
        :return: Error
        """
        request = requests.delete(self.API_URL['delete'].format(f'?group_id={group_id}&customer_id={customer_id}'))
        
        if request.status_code == 204:
            return Error(False, None)
        else:
            return Error(True, request.status_code)

    def to_create_request_data(self, data):
        request_data = {
            'group': data.group,
            'customer': data.customer
        }
        return request_data


from Base.base_dao import BaseDAO, BASE_API_URL
from DTO.staff import Staff, GroupStaff, StaffType
from Base.error import Error
from DAO.group import GroupDAO
import requests

class StaffDAO(BaseDAO):
    DTO_CLASS = Staff
    API_URL = {
        'read':         f'{BASE_API_URL}/staff',
        'create':       f'{BASE_API_URL}/staff/',
        'read_detail':  f'{BASE_API_URL}/staff/{{}}',
        'update':       f'{BASE_API_URL}/staff/{{}}',
        'delete':       f'{BASE_API_URL}/staff/{{}}'
    }

    def to_create_request_data(self, data):
        request_data = {
            'name': data.name
        }
        return request_data

class StaffTypeDAO(BaseDAO):
    DTO_CLASS = StaffType
    API_URL = {
        'read':         f'{BASE_API_URL}/staff/staff_type',
        'create':       f'{BASE_API_URL}/staff/staff_type/',
        'read_detail':  f'{BASE_API_URL}/staff/staff_type/{{}}',
        'update':       f'{BASE_API_URL}/staff/staff_type/{{}}',
        'delete':       f'{BASE_API_URL}/staff/staff_type/{{}}'
    }

    def to_create_request_data(self, data):
        request_data = {
            'name': data.name
        }
        return request_data
        

class GroupStaffDAO(BaseDAO):
    DTO_CLASS = GroupStaff
    API_URL = {
        'read':         f'{BASE_API_URL}/staff/group/{{}}',
        'create':       f'{BASE_API_URL}/staff/group/',
        'read_detail':  f'{BASE_API_URL}/staff/group/{{}}',
        'update':       f'{BASE_API_URL}/staff/group/{{}}',
        'delete':       f'{BASE_API_URL}/staff/group/{{}}'
    }
    group_dao = GroupDAO()
    staff_dao = StaffDAO()
    staff_type_dao = StaffTypeDAO()
    
    def get_object(self, data):
        _, data['group'] = self.group_dao.read_detail(data['group'])
        _, data['staff'] = self.staff_dao.read_detail(data['staff'])
        _, data['staff_type'] = self.staff_type_dao.read_detail(data['staff_type'])
        return self.DTO_CLASS(**data)

    def to_create_request_data(self, data):
        request_data = {
            'group': data.group.id,
            'staff': data.staff.id,
            'staff_type': data.staff_type.id
        }
        return request_data

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
    
    def delete(self, group_id: int, staff_id: int) -> Error:
        """
        Delete method in DAO, equivalent to delete method (destroy action)
        :tour_id: int -> Tour id
        :return: Error
        """
        request = requests.delete(self.API_URL['delete'].format(f'?group_id={group_id}&staff_id={staff_id}'))
        
        if request.status_code == 204:
            return Error(False, None)
        else:
            return Error(True, request.status_code)
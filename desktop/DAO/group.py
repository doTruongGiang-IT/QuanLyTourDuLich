import requests
from datetime import date, datetime
from Base.base_dao import BaseDAO, BASE_API_URL
from Base.error import Error
from DTO.group import Group, GroupJourney

class GroupDAO(BaseDAO):
    DTO_CLASS = None
    API_URL = {
        'read': f'{BASE_API_URL}/group',
        'read_detail': f'{BASE_API_URL}/group/{{}}',
        'create': f'{BASE_API_URL}/group',
        'update': f'{BASE_API_URL}/group/{{}}',
        'delete': f'{BASE_API_URL}/group/{{}}'
    }
    
    def get_object(self, data):
        data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%d')
        data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%d')
        return self.DTO_CLASS(**data)

    def to_create_request_data(self, data):
        request_data = {
            'name': data.name,
            'start_date': data.start_date,
            'end_date': data.end_date,
            'journey': data.joourney
        }

        return request_data

    
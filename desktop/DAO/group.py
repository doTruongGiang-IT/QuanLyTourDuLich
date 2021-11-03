from datetime import datetime

from Base.base_dao import BASE_API_URL, BaseDAO
from DTO.group import Group, GroupJourney

from DAO.tour import LocationDAO


class GroupJourneyDAO(BaseDAO):
    DTO_CLASS = GroupJourney
    API_URL = {
        'read':         f'{BASE_API_URL}/group/journey',
        'create':       f'{BASE_API_URL}/group/journey',
        'read_detail':  f'{BASE_API_URL}/group/journey/{{}}',
        'update':       f'{BASE_API_URL}/group/journey/{{}}',
        'delete':       f'{BASE_API_URL}/group/journey/{{}}'
    }
    location_dao = LocationDAO()

    def get_object(self, data):
        data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%dT%H:%M:%SZ')
        data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%dT%H:%M:%SZ')
        data['location'] = self.__class__.location_dao.get_object(data['location'])
        return self.DTO_CLASS(**data)

    def to_create_request_data(self, data):
        request_data = {
            'group': data.group,
            'content': data.content,
            'start_date': data.start_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'end_date': data.end_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
            'location': data.location.id
        }

        return request_data


class GroupDAO(BaseDAO):
    DTO_CLASS = Group
    API_URL = {
        'read':         f'{BASE_API_URL}/group',
        'create':       f'{BASE_API_URL}/group/',
        'read_detail':  f'{BASE_API_URL}/group/{{}}',
        'update':       f'{BASE_API_URL}/group/{{}}',
        'delete':       f'{BASE_API_URL}/group/{{}}'
    }
    journey_dao = GroupJourneyDAO()
    
    def get_object(self, data):
        data['start_date'] = datetime.strptime(data['start_date'], '%Y-%m-%d')
        data['end_date'] = datetime.strptime(data['end_date'], '%Y-%m-%d')
        journeys = []
        for journey in data['journey']:
            journeys.append(self.__class__.journey_dao.get_object(journey))
            
        data['journey'] = journeys

        return self.DTO_CLASS(**data)

    def to_create_request_data(self, data):
        request_data = {
            'name': data.name,
            'tour': data.tour,
            'start_date': data.start_date.strftime("%Y-%m-%d"),
            'end_date': data.end_date.strftime("%Y-%m-%d"),
        }

        return request_data
    
    def create(self, data):
        error = super().create(data)
        
        if error.status is False:
            for journey in data.journey:
                journey_error = self.__class__.journey_dao.create(journey)
                if journey_error.status is True:
                    error.status = journey_error
                    break
                
        return error

from datetime import datetime
from Base.base_dao import BaseDAO, BASE_API_URL
from DTO.statistics import StatsToursOfStaff

    
class StatsToursOfStaffDAO(BaseDAO):
    DTO_CLASS = StatsToursOfStaff
    API_URL = {
        'read':         f'{BASE_API_URL}/stats/tour_of_staff',
    }
    
    # def to_create_request_data(self, data):
    #     request_data = {
    #         'name': data.name
    #     }
    #     return request_data
    

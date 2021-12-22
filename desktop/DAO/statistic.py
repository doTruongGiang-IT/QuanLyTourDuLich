import requests
from Base.base_dao import BaseDAO, BASE_API_URL
from DTO.statistic import StatsCostRevenueTour, StatsCostRevenueGroup, StatsToursOfStaff
from DAO.tour import TourCharacteristicDAO, TourTypeDAO, TourPriceDAO, LocationDAO
from Base.error import Error

class StatsCostRevenueTourDAO(BaseDAO):
    DTO_CLASS = StatsCostRevenueTour
    API_URL = {
        'read':         f'{BASE_API_URL}/stats/stats_cost_revenue_tour',
        'read_detail':  f'{BASE_API_URL}/stats/stats_cost_revenue_tour/{{}}'
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
            'location': data.location.id,
            'cost': data.cost,
            'revenue': data.revenue
        }
        return request_data

class StatsCostRevenueGroupDAO(BaseDAO):
    DTO_CLASS = StatsCostRevenueGroup
    API_URL = {
        'read':         f'{BASE_API_URL}/stats/stats_cost_revenue_group/{{}}',
        'read_detail':  f'{BASE_API_URL}/stats/stats_cost_revenue_group/{{}}'
    }

    def read(self, tour_id) -> tuple[Error, list[DTO_CLASS]]:
        """
        Read method in DAO, equivalent to GET method (get list action)
        :return: tuple[Error, list[DTO_CLASS]]
        """
        request = requests.get(self.API_URL['read'].format(tour_id))
    
        if request.status_code == 200:
            response = request.json()
            result = []
            print(response)
            for data in response:
                result.append(self.get_object(data))
            print(result)
            return (Error(False, None), result)
        else:
            return (Error(True, 'Get the tour list that have an error'), None)
    
class StatsToursOfStaffDAO(BaseDAO):
    DTO_CLASS = StatsToursOfStaff
    API_URL = {
        'read':         f'{BASE_API_URL}/stats/tour_of_staff',
        'read_detail':  f'{BASE_API_URL}/stats/tour_of_staff/{{}}'
    }

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
    

from Base.base_bus import BaseBUS
from DAO.statistic import StatsToursOfStaffDAO, StatsCostRevenueTourDAO, StatsCostRevenueGroupDAO
from DTO.statistic import StatsToursOfStaff, StatsCostRevenueTour, StatsCostRevenueGroup

class StatsToursOfStaffBUS(BaseBUS):
    DTO_CLASS = StatsToursOfStaff
    DAO_CLASS = StatsToursOfStaffDAO
    
class StatsCostRevenueTourBUS(BaseBUS):
    DTO_CLASS = StatsCostRevenueTour
    DAO_CLASS = StatsCostRevenueTourDAO

class StatsCostRevenueGroupBUS(BaseBUS):
    DTO_CLASS = StatsCostRevenueGroup
    DAO_CLASS = StatsCostRevenueGroupDAO

    def read(self, group_id) -> list[DTO_CLASS]:
        """
        Read method in BUS, equivalent to GET method (get list action)
        :return: list[DTO_CLASS]:
        """
        error, objects = self.query.read(group_id)
        if error.status is True:
            print(error.message)
            return None
        
        return objects

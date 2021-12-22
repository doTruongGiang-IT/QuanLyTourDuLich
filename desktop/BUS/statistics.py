from Base.base_bus import BaseBUS
from DAO.statistics import StatsToursOfStaffDAO
from DTO.statistics import StatsToursOfStaff


class StatsToursOfStaffBUS(BaseBUS):
    DTO_CLASS = StatsToursOfStaff
    DAO_CLASS = StatsToursOfStaffDAO
    
    


from Base.base_bus import BaseBUS
from DAO.tour import TourCharacteristicDAO, TourTypeDAO, TourPriceDAO, LocationDAO, TourDAO
from DTO.tour import TourCharacteristic, TourType, TourPrice, Location, Tour


class TourCharacteristicBUS(BaseBUS):
    DTO_CLASS = TourCharacteristic
    DAO_CLASS = TourCharacteristicDAO
    
    
class TourTypeBUS(BaseBUS):
    DTO_CLASS = TourType
    DAO_CLASS = TourTypeDAO
    
    
class TourPriceBUS(BaseBUS):
    DTO_CLASS = TourPrice
    DAO_CLASS = TourPriceDAO
    
    
class LocationBUS(BaseBUS):
    DTO_CLASS = Location
    DAO_CLASS = LocationDAO
    
    
class TourBUS(BaseBUS):
    DTO_CLASS = Tour
    DAO_CLASS = TourDAO
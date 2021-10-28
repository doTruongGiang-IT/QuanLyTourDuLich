from Base.base_bus import BaseBUS
from DAO.tour import TourCharacteristicDAO
from DTO.tour import TourCharacteristic


class TourCharacteristicBUS(BaseBUS):
    DTO_CLASS = TourCharacteristic
    DAO_CLASS = TourCharacteristicDAO
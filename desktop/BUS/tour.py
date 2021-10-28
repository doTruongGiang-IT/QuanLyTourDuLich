from desktop.DAO.tour_characteristic import TourCharacteristicDAO
from desktop.DTO.tour import TourCharacteristic

class TourCharacteristicBUS:
    def __init__(self):
        self.objects = []
        self.query = TourCharacteristicDAO()
        
    def read(self):
        error, self.objects = self.query.read()
        if error:
            print(error)
            
    def create(self, tour_characteristic: TourCharacteristic):
        error = self.query.create(tour_characteristic)
        if error:
            print(error)
            
    def update(self, tour_characterictic: TourCharacteristic):
        error = self.query.update(tour_characterictic)
        if error:
            print(error)
            
    def delete(self, tour_characteristic_id: int):
        error = self.query.delete(tour_characteristic_id)
        if error:
            print(error)
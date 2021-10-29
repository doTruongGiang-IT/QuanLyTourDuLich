from datetime import datetime


class TourCharacteristic:
    def __init__(
        self,
        id: int,
        name: str
    ):
        self.id             = id
        self.name           = name
        
    def __str__(self):
        return str({
            'id': self.id,
            'name': self.name
        })
        
        
class TourType:
    def __init__(
        self,
        id: int,
        name: str
    ):
        self.id             = id
        self.name           = name
        
        
class TourPrice:
    def __init__(
        self,
        id: int,
        name: str,
        price: int,
        start_date: datetime,
        end_date: datetime
    ):
        self.id             = id
        self.name           = name
        self.price          = price
        self.start_date     = start_date
        self.end_date       = end_date
        
        
class Location:
    def __init__(
        self,
        id: int,
        name: str,
        type: str
    ):
        self.id             = id
        self.name           = name
        self.type           = type
        
        
class Tour:
    def __init__(
        self,
        id: int,
        name: str,
        characteristic: TourCharacteristic,
        type: TourType,
        price: TourPrice,
        location: Location
    ):
        self.id             = id 
        self.name           = name 
        self.characteristic = characteristic 
        self.type           = type 
        self.price          = price 
        self.location       = location
        

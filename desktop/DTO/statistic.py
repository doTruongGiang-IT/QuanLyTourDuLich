
from DTO.tour import TourCharacteristic, TourType, TourPrice, Location

class StatsCostRevenueTour:
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        characteristic: TourCharacteristic,
        type: TourType,
        price: TourPrice,
        location: Location,
        cost: float,
        revenue: float
    ):
        self.id = id
        self.name = name
        self.description = description
        self.characteristic = characteristic
        self.type = type
        self.price = price
        self.location = location
        self.cost = cost
        self.revenue = revenue

class StatsCostRevenueGroup:
    def __init__(
        self,
        id: int,
        name: str,
        revenue: float,
        cost: float
    ):
        self.id = id
        self.name = name
        self.revenue = revenue
        self.cost = cost

class StatsToursOfStaff:
    def __init__(
        self,
        id: int,
        name: str,
        number_of_tours: int
    ):
        self.id = id
        self.name = name
        self.number_of_tours = number_of_tours
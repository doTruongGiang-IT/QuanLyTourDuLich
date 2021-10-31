from datetime import date, datetime

from desktop.DTO.tour import Location
from tour import Location

class GroupJourney:
    def __init__(self, id: int, content: str, start_date: datetime, end_date: datetime, location: Location):
        self.id = id
        self.content = content
        self.start_date = start_date
        self.end_date = end_date
        self.location = location

class Group:
    def __init__(self, id: int, name: str, start_date: datetime, end_date: datetime, journey: list[GroupJourney]):
        self.id = id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.journey = journey

from datetime import datetime

from DTO.tour import Location


class GroupJourney:
    def __init__(
        self,
        id: int,
        group: int,
        content: str, 
        start_date: datetime, 
        end_date: datetime, 
        location: Location
    ):
        self.id = id
        self.group = group
        self.content = content
        self.start_date = start_date
        self.end_date = end_date
        self.location = location


class Group:
    def __init__(
        self, 
        id: int, 
        name: str,
        tour: int,
        start_date: datetime, 
        end_date: datetime, 
        revenue: int,
        journey: list[GroupJourney]
    ):
        self.id = id
        self.name = name
        self.tour = tour
        self.start_date = start_date
        self.end_date = end_date
        self.revenue = revenue
        self.journey = journey

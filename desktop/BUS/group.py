from Base.base_bus import BaseBUS
from DAO.group import GroupDAO, GroupJourneyDAO
from DTO.group import Group, GroupJourney


class GroupBUS(BaseBUS):
    DTO_CLASS = Group
    DAO_CLASS = GroupDAO

class GroupJourneyBUS(BaseBUS):
    DTO_CLASS = GroupJourney
    DAO_CLASS = GroupJourneyDAO

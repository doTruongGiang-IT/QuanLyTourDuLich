from Base.base_bus import BaseBUS
from DTO.group import Group
from DAO.group import GroupDAO
from desktop.DAO.group import GroupJourneyDAO
from desktop.DTO.group import GroupJourney

class GroupBUS(BaseBUS):
    DTO_CLASS = Group
    DAO_CLASS = GroupDAO

class GroupJourneyBUS(BaseBUS):
    DTO_CLASS = GroupJourney
    DAO_CLASS = GroupJourneyDAO
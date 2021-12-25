from Base.base_bus import BaseBUS
from DAO.group import GroupDAO, GroupJourneyDAO, GroupCostTypeDAO, GroupCostDAO
from DTO.group import Group, GroupJourney, GroupCostType, GroupCost


class GroupBUS(BaseBUS):
    DTO_CLASS = Group
    DAO_CLASS = GroupDAO

class GroupJourneyBUS(BaseBUS):
    DTO_CLASS = GroupJourney
    DAO_CLASS = GroupJourneyDAO

class GroupCostTypeBUS(BaseBUS):
    DTO_CLASS = GroupCostType
    DAO_CLASS = GroupCostTypeDAO

class GroupCostBUS(BaseBUS):
    DTO_CLASS = GroupCost
    DAO_CLASS = GroupCostDAO
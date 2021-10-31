from Base.base_bus import BaseBUS
from DTO.group import Group
from DAO.group import GroupDAO

class GroupBUS(BaseBUS):
    DTO_CLASS = Group
    DAO_CLASS = GroupDAO
from Base.base_bus import BaseBUS
from DAO.staff import GroupStaffDAO, StaffDAO, StaffTypeDAO, GroupStaffDAO
from DTO.staff import GroupStaff, Staff, StaffType, GroupStaff
from Base.error import Error

class StaffBUS(BaseBUS):
    DTO_CLASS = Staff
    DAO_CLASS = StaffDAO

class StaffTypeBUS(BaseBUS):
    DTO_CLASS = StaffType
    DAO_CLASS = StaffTypeDAO

class GroupStaffBUS(BaseBUS):
    DTO_CLASS = GroupStaff
    DAO_CLASS = GroupStaffDAO

    def group_objects(self, group_id) -> list[DTO_CLASS]:
        return self.read(group_id)

    def read(self, group_id) -> list[DTO_CLASS]:
        """
        Read method in BUS, equivalent to GET method (get list action)
        :return: list[DTO_CLASS]:
        """
        error, objects = self.query.read(group_id)
        if error.status is True:
            print(error.message)
            return None
        
        return objects

    def delete(self, group_id: int, staff_id: int) -> Error:
        """
        Create method in BUS, equivalent to POST method (create action)
        :obj: DTO_CLASS 
        :return: Error:
        """
        error = self.query.delete(group_id, staff_id)
        if error.status is True:
            print(error.message)
        return error

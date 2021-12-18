from DTO.group import Group


class Staff:
    def __init__(
        self,
        id: int,
        name: str
    ):
        self.id = id
        self.name = name

class StaffType:
    def __init__(
        self,
        id: int,
        name: str
    ):
        self.id = id
        self.name = name

class GroupStaff:
    def __init__(
        self,
        id: int,
        group: Group,
        staff: Staff,
        staff_type: StaffType
    ):
        self.id = id
        self.group = group
        self.staff = staff
        self.staff_type = staff_type
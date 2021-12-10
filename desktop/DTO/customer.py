
class Customer:
    def __init__(
        self,
        id: int,
        name: str,
        id_number: str,
        address: str,
        gender: str,
        phone_number: str
        ):
        self.id = id
        self.name = name
        self.id_number = id_number
        self.address = address
        self.gender = gender
        self.phone_number = phone_number

class GroupCustomer:
    def __init__(
        self,
        id: int,
        group: int,
        customer: int
        ):
        self.id = id
        self.group = group
        self.customer = customer



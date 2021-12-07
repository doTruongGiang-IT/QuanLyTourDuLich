from Base.base_bus import BaseBUS
from DAO.customer import CustomerDAO
from DTO.customer import Customer

class CustomerBUS(BaseBUS):
    DTO_CLASS = Customer
    DAO_CLASS = CustomerDAO
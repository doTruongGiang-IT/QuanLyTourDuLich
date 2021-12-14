from Base.base_bus import BaseBUS
from DAO.customer import CustomerDAO, GroupCustomerDAO
from DTO.customer import Customer, GroupCustomer
from Base.error import Error

class CustomerBUS(BaseBUS):
    DTO_CLASS = Customer
    DAO_CLASS = CustomerDAO

class GroupCustomerBUS(BaseBUS):
    DTO_CLASS = GroupCustomer
    DAO_CLASS = GroupCustomerDAO

    @property
    def objects(self, group_id) -> list[DTO_CLASS]:
        if self.__class__.TRACKING_STATUS is False:
            self.__class__.TRACKING_STATUS = True
            self.__class__.STORED_OBJECTS = self.read(group_id)
        
        return self.__class__.STORED_OBJECTS

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

    def delete(self, group_id: int, customer_id: int) -> Error:
        """
        Create method in BUS, equivalent to POST method (create action)
        :obj: DTO_CLASS 
        :return: Error:
        """
        error = self.query.delete(group_id, customer_id)
        if error.status is True:
            print(error.message)
        return error

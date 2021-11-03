from typing import Tuple
from Base.error import Error


class BaseBUS:
    DTO_CLASS = None
    DAO_CLASS = None
    
    # These are for lazy loading
    STORED_OBJECTS = None
    TRACKING_STATUS = False
    
    def __init__(self):
        self.query = self.DAO_CLASS()
        
    @property
    def objects(self) -> list[DTO_CLASS]:
        if self.__class__.TRACKING_STATUS is False:
            self.__class__.TRACKING_STATUS = True
            self.__class__.STORED_OBJECTS = self.read()
        
        return self.__class__.STORED_OBJECTS
        
    def read(self) -> list[DTO_CLASS]:
        """
        Read method in BUS, equivalent to GET method (get list action)
        :return: list[DTO_CLASS]:
        """
        error, objects = self.query.read()
        if error.status is True:
            print(error.message)
            return None
        
        return objects
            
    def create(self, obj: DTO_CLASS) -> Error:
        """
        Create method in BUS, equivalent to POST method (create action)
        :obj: DTO_CLASS 
        :return: Error:
        """
        error = self.query.create(obj)
        if error.status is True:
            print(error.message)
        return error
            
    def update(self, obj: DTO_CLASS) -> Error:
        """
        Update method in BUS, equivalent to PATCH method (partial_update action)
        :obj: DTO_CLASS 
        :return: Error:
        """
        error = self.query.update(obj)
        if error.status is True:
            print(error.message)
        return error
            
    def delete(self, obj_id: int) -> Error:
        """
        Create method in BUS, equivalent to POST method (create action)
        :obj: DTO_CLASS 
        :return: Error:
        """
        error = self.query.delete(obj_id)
        if error.status is True:
            print(error.message)
        return error
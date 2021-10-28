class BaseBUS:
    DTO_CLASS = None
    DAO_CLASS = None
    
    def __init__(self):
        self.query = self.DAO_CLASS()
        
    @property
    def objects(self):
        return self.read()
        
    def read(self) -> list[DTO_CLASS]:
        error, objects = self.query.read()
        if error:
            print(error)
            return None
        else:
            return objects
            
    def create(self, obj: DTO_CLASS) -> None:
        error = self.query.create(obj)
        if error:
            print(error)
            
    def update(self, obj: DTO_CLASS) -> None:
        error = self.query.update(obj)
        if error:
            print(error)
            
    def delete(self, obj_id: int) -> None:
        error = self.query.delete(obj_id)
        if error:
            print(error)
from .component import Component

class Singleton:
    def __new__(cls,*a, **b):
        if hasattr(cls,'_inst'):
            return cls._inst
        else:
            cls._inst=super().__new__(cls,*a,**b)
            return cls._inst

class Repo(Singleton):
    _objects = {}  # Map<Int(id), Component>
    _attached_objects = {}  # Map<String(user), List<Int(id)>>
    _id = 0  # ID counter

    @staticmethod
    def create(*p, **kw): # Creates a new object with a unique ID and stores it in the Repo
        Repo._objects[Repo._id] = p
        Repo._id += 1

    @staticmethod
    def list(): # Lists all objects with their ID and description
        print( [(obj_id, str(obj)) for obj_id, obj in Repo._objects.items()] )
    
    @staticmethod
    def listattached(user: str):
        try:
            print( Repo._attached_objects[user] )
        except KeyError:
            print("User not found")


    @staticmethod
    def attach(obj_id: int, user: str): # Attaches a user to an object
        if user not in Repo._attached_objects.keys():
            Repo._attached_objects[user] = []
        Repo._attached_objects[user].append(obj_id)

    @staticmethod
    def detach(obj_id: int, user: str): # Detaches a user from an object
        Repo._attached_objects[user].remove(obj_id)

    @staticmethod
    def delete(obj_id: int): # Deletes an object by ID
        for user in Repo._attached_objects.keys():
            if obj_id in Repo._attached_objects[user]:
                Repo._attached_objects[user].remove(obj_id)

        if obj_id in Repo._objects:
            del Repo._objects[obj_id]

    @property
    def components(self):
        return Component

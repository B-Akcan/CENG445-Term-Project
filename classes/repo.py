from .component import Component
from .map import Map

class Singleton:
    def __new__(cls,*a, **b):
        if hasattr(cls,'_inst'):
            return cls._inst
        else:
            cls._inst=super().__new__(cls,*a,**b)
            return cls._inst

class Repo(Singleton):
    _objects = {}  # Dict<Int(id), Map>
    _attached_objects = {}  # Dict<String(user), List<Int(id)>>
    _id = 0  # ID counter

    @staticmethod
    def create(**kw) -> int: # Creates a new map object with a unique ID and stores it in the Repo
        assigned_id = Repo._id
        Repo._objects[assigned_id] = Map(**kw)
        Repo._id += 1
        return assigned_id

    @staticmethod
    def list() -> None: # Lists all objects with their ID and description
        print( [(obj_id, str(obj)) for obj_id, obj in Repo._objects.items()] )
    
    @staticmethod
    def listattached(user: str) -> None:
        try:
            print( Repo._attached_objects[user] )
        except KeyError:
            print("User not found")

    @staticmethod
    def attach(obj_id: int, user: str) -> None: # Attaches an object to a user
        if obj_id not in Repo._objects.keys():
            raise ValueError(f"Object with id '{obj_id}' does not exist")
        if user not in Repo._attached_objects.keys():
            Repo._attached_objects[user] = []
        Repo._attached_objects[user].append(obj_id)

    @staticmethod
    def detach(obj_id: int, user: str) -> None: # Detaches an object from a user
        Repo._attached_objects[user].remove(obj_id)

    @staticmethod
    def delete(obj_id: int) -> None: # Deletes an object by ID
        for user in Repo._attached_objects.keys():
            if obj_id in Repo._attached_objects[user]:
                Repo._attached_objects[user].remove(obj_id)

        if obj_id in Repo._objects:
            del Repo._objects[obj_id]

    @property
    def components(self):
        return Component
    
    @staticmethod
    def getObjectOfUser(id: int, user: str) -> Map | None:
        if id in Repo._attached_objects[user]:
            return Repo._objects[id]
        raise ValueError(f"Object with id '{id}' is not attached to user '{user}'")


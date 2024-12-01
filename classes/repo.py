from .component import Component
from .map import Map
from .singleton import Singleton
import json

class Repo(Singleton):
    _maps = {}  # Dict<Int(id), Map>
    _attached_maps = {}  # Dict<String(user), List<Int(id)>>
    _id = 0  # ID counter

    @staticmethod
    def create(**kw) -> int: # Creates a new map object with a unique ID and stores it in the Repo
        assigned_id = Repo._id
        Repo._maps[assigned_id] = Map(**kw)
        Repo._id += 1
        return assigned_id

    @staticmethod
    def list() -> None: # Lists all maps with their ID and description
        print( [(map_id, str(map)) for map_id, map in Repo._maps.items()] )
    
    @staticmethod
    def listattached(user: str) -> None:
        try:
            print( Repo._attached_maps[user] )
        except KeyError:
            print("User not found")

    @staticmethod
    def attach(map_id: int, user: str) -> None: # Attaches a map to a user
        if map_id not in Repo._maps:
            raise ValueError(f"Map with id '{map_id}' does not exist")
        if user not in Repo._attached_maps:
            Repo._attached_maps[user] = []
        Repo._attached_maps[user].append(map_id)

    @staticmethod
    def detach(map_id: int, user: str) -> None: # Detaches a map from a user
        Repo._attached_maps[user].remove(map_id)

    @staticmethod
    def delete(map_id: int) -> None: # Deletes a map by ID
        for user in Repo._attached_maps:
            if map_id in Repo._attached_maps[user]:
                Repo._attached_maps[user].remove(map_id)

        if map_id in Repo._maps:
            del Repo._maps[map_id]

    @property
    def components(self):
        return Component
    
    @staticmethod
    def getMapOfUser(id: int, user: str) -> Map | None:
        if id in Repo._attached_maps[user]:
            return Repo._maps[id]
        raise ValueError(f"Map with id '{id}' is not attached to user '{user}'")
    
    @staticmethod
    def addUser(username: str) -> None:
        if username not in Repo._attached_maps:
            Repo._attached_maps[username] = []
    
    @staticmethod
    def saveMap(map_id: int) -> None:
        if map_id in Repo._maps:
            with open(f"./maps/map{map_id}", "w") as file:
                file.write(json.dumps(Repo._maps[map_id].to_dict(), indent=4))
        else:
            print(f"No map with id {map_id} exist.")

    @staticmethod
    def loadMap(map_id: int) -> Map:
        try: # if map is saved before
            with open(f"./maps/map{map_id}", "r") as file:
                return json.loads(file)
        except:
            if map_id in Repo._maps:
                return Repo._maps[map_id]
            else:
                print(f"No map with id {map_id} exist.")
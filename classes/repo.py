from .singleton import Singleton
from .map import Map
from .component import Component
import json
from pathlib import Path

class Repo(Singleton):
    _maps = {}  # Dict<Int(id), Map>
    _attached_maps = {}  # Dict<String(user), List<Int(id)>>
    _id = 0  # ID counter

    @staticmethod
    def create(**kw) -> int: # Creates a new map object with a unique ID and stores it in the Repo
        assigned_id = Repo._id
        Repo._maps[assigned_id] = Map(**kw)
        Repo._id += 1
        Repo.saveMap(assigned_id)
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
    def saveRegisteredComponents() -> None:
        root = Path(__file__).parent
        path_to_create = root / "saved" / "registered_components.txt"
        with path_to_create.open("w") as file:
            for comp in Repo().components.registeredComponentsToList():
                file.write(comp + "\n")

    @staticmethod
    def loadRegisteredComponents() -> None:
        try:
            root = Path(__file__).parent
            path_to_read = root / "saved" / "registered_components.txt"
            with path_to_read.open("r") as file:
                temp = file.read().split("\n")[:-1]
                for e in temp:
                    Repo().components.register(e)
        except:
            pass

    @staticmethod
    def delete(map_id: int) -> None: # Deletes a map by ID
        # Detach from all users
        for user in Repo._attached_maps:
            if map_id in Repo._attached_maps[user]:
                Repo._attached_maps[user].remove(map_id)

        if map_id in Repo._maps:
            del Repo._maps[map_id]

        Repo.deleteMap(map_id)

    @property
    def components(self):
        return Component
    
    @staticmethod
    def addUser(username: str) -> None:
        if username not in Repo._attached_maps:
            Repo._attached_maps[username] = []
    
    @staticmethod
    def saveMap(map_id: int) -> None:
        if map_id in Repo._maps:
            root = Path(__file__).parent
            path_to_create = root / "saved" / "maps" / f"map{map_id}.json"
            with path_to_create.open("w") as file:
                file.write(json.dumps(Repo._maps[map_id].to_dict(), indent=4))

    @staticmethod
    def loadMap(map_id: int):
        try: # if map is saved before
            root = Path(__file__).parent
            path_to_read = root / "saved" / "maps" / f"map{map_id}.json"
            with path_to_read.open("r") as file:
                return json.loads(file.read())
        except:
            return None

    @staticmethod
    def deleteMap(map_id: int) -> None:
        try:
            root = Path(__file__).parent
            path_to_delete = root / "saved" / "maps" / f"map{map_id}.json"
            path_to_delete.unlink()
        except FileNotFoundError:
            pass
        
    @staticmethod
    def deleteAllMaps() -> None:
        i = 0
        while True:
            try:
                root = Path(__file__).parent
                path_to_delete = root / "saved" / "maps" / f"map{i}.json"
                path_to_delete.unlink()
                i += 1
            except FileNotFoundError:
                break

    @staticmethod
    def getAllMaps():
        return list(Repo._maps.keys())
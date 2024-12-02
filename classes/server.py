import socket
import threading as th
from .repo import Repo

class Server:
    def __init__(self, host: str, port: int):
        self.host: str = host
        self.port: int = port
        self.agents: list[Agent] = []

    def start_server(self) -> None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            ns, addr = s.accept()
            print(f"Connection established with {addr}")
            agent = Agent(socket=ns)
            agent.start()

class Agent(th.Thread): # server thread that handles user request
    def __init__(self, socket, username=""):
        super().__init__()
        self.username = username # user to be communicated
        self.socket = socket # server socket that communicates with user

    def run(self):
        message = self.socket.recv(1024)
        while message != "":
            try:
                msg = message.decode().strip()
                self.process_command(msg)
            except UnicodeDecodeError as e:
                self.socket.send(str(e).encode())
            message = self.socket.recv(1024)

    def process_command(self, command: str) -> None:
        args = command.split()
        if args[0] == "USER":
            if len(args) != 2:
                self.socket.send("Please provide a username.")
            else:
                self.username = args[1]
                Repo.addUser(self.username)
                self.socket.send(f"Username set to {self.username}.\n".encode())
        elif args[0] == "ATTACH_MAP":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 2:
                    self.socket.send(b"Please provide a map id.\n")
                else:
                    map_id = int(args[1])
                    Repo.attach(map_id, self.username)
                    self.socket.send(f"Map {map_id} attached to user {self.username}.\n".encode())
        elif args[0] == "DETACH_MAP":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 2:
                    self.socket.send(b"Please provide a map id.\n")
                else:
                    map_id = int(args[1])
                    Repo.detach(map_id, self.username)
                    self.socket.send(f"Map {map_id} detached from user {self.username}.\n".encode())
        elif args[0] == "START_GAME":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 2:
                    self.socket.send(b"Please provide a map id.\n")
                else:
                    map_id = int(args[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        _map = Repo.loadMap(map_id)
                        _map.start()
                        self.socket.send(b"Game started.\n")
        elif args[0] == "STOP_GAME":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 2:
                    self.socket.send(b"Please provide a map id.\n")
                else:
                    map_id = int(args[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        Repo._maps[map_id].stop()
                        self.socket.send(b"Game stopped.\n")
        elif args[0] == "SAVE":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 2:
                    self.socket.send(b"Please provide a map id.\n")
                else:
                    map_id = int(args[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        Repo.saveMap(map_id)
                        self.socket.send(b"Map saved.\n")
        elif args[0] == "CREATE_MAP":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 5:
                    self.socket.send(b"Please provide number of columns (int), number of rows (int), cellsize (int), background color (string).\n")
                else:
                    cols, rows, cellsize = map(int, args[1:4])
                    bgcolor = args[4]
                    map_id = Repo.create(cols=cols, rows=rows, cellsize=cellsize, bgcolor=bgcolor)
                    Repo.attach(map_id, self.username)
                    self.socket.send(f"Map created with id {map_id} and attached to user {self.username}.\n".encode())
        elif args[0] == "DELETE_MAP":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 2:
                    self.socket.send(b"Please provide map id.\n")
                else:
                    map_id = int(args[1])
                    Repo.delete(map_id)
                    self.socket.send(f"Map with id {map_id} was detached from all users and deleted.\n")
        elif args[0] == "REGISTER_COMP":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 2:
                    self.socket.send(b"Please provide component type.\n")
                else:
                    comp = args[1]
                    try:
                        Repo().components.register(comp)
                        self.socket.send(f"Component {comp} registered.\n".encode())
                    except ValueError as e:
                        self.socket.send(str(e).encode())
        elif args[0] == "UNREGISTER_COMP":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 2:
                    self.socket.send(b"Please provide component type.\n")
                else:
                    comp = args[1]
                    try:
                        Repo().components.unregister(comp)
                        self.socket.send(f"Component {comp} unregistered.\n".encode())
                    except ValueError as e:
                        self.socket.send(str(e).encode())
        elif args[0] == "REGISTER_ALL_COMPS":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                Repo().components.registerAll()
                self.socket.send(b"All components registered.\n")
        elif args[0] == "CREATE_COMP":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 5:
                    self.socket.send(b"Please provide map id (int), component name (str), x coordinate (int), y coordinate (int).\n")
                else:
                    map_id = int(args[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        comp = args[2]
                        x, y = map(int, args[3:5])
                        _map = Repo._maps[map_id]
                        try:
                            _map[(x, y)] = Repo().components.create(comp)
                            self.socket.send(f"Component '{comp}' created at ({x},{y}) of map with id {map_id}.\n".encode())
                        except ValueError as e:
                            self.socket.send(str(e).encode())
        elif args[0] == "ROTATE_COMP":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 4:
                    self.socket.send(b"Please provide map id (int), x coordinate (int), y coordinate (int).\n")
                else:
                    map_id = int(args[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        x, y = map(int, args[2:4])
                        _map = Repo._maps[map_id]
                        _map[(x, y)].rotation = (_map[(x, y)].rotation + 1) % 4
                        self.socket.send(f"Component at ({x},{y}) of map {map_id} was rotated.\n".encode())
        elif args[0] == "DELETE_COMP":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 4:
                    self.socket.send(b"Please provide map id (int), x coordinate (int), y coordinate (int).\n")
                else:
                    map_id = int(args[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        x, y = map(int, args[2:4])
                        _map = Repo._maps[map_id]
                        try:
                            del _map[(x, y)]
                            self.socket.send(b"Component deleted.\n")
                        except IndexError as e:
                            self.socket.send(str(e).encode())
                        except KeyError as e:
                            self.socket.send((str(e).replace("'", "") + "\n").encode())
        elif args[0] == "CREATE_CAR":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 8:
                    self.socket.send(b"Please provide map id (int), model (str), driver (str), x (int), y (int), topspeed (int), topfuel (int).\n")
                else:
                    map_id = int(args[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        try:
                            x, y, topspeed, topfuel = map(int, args[4:8])
                            model, driver = args[2:4]
                            _map = Repo._maps[map_id]
                            car = Repo().components.create("Car", model=model, map_ref=_map, driver=driver, pos=(x,y), angle=0, topspeed=topspeed, topfuel=topfuel)
                            car_id = _map.place(car, x, y)
                            self.socket.send(f"Car created with id {car_id}.\n".encode())
                        except ValueError as e:
                            self.socket.send(str(e).encode())
        elif args[0] == "DELETE_CAR":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 3:
                    self.socket.send(b"Please provide map id (int), car id (int).\n")
                else:
                    map_id = int(args[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        _map = Repo._maps[map_id]
                        car_id = int(args[2])
                        try:
                            _map.remove_car(car_id)
                            self.socket.send(f"Car with id {car_id} deleted.\n".encode())
                        except KeyError as e:
                            self.socket.send((str(e).replace("'", "") + "\n").encode())
        elif args[0] == "START_CAR":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 3:
                    self.socket.send(b"Please provide map id (int), car id (int).\n")
                else:
                    map_id = int(args[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        _map = Repo._maps[map_id]
                        car_id = int(args[2])
                        if car_id in _map.cars:
                            _map.cars[car_id].start()
                            self.socket.send(f"Car with {car_id} started.\n".encode())
                        else:
                            self.socket.send(f"Car with id {car_id} does not exist.\n".encode())
        elif args[0] == "STOP_CAR":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 3:
                    self.socket.send(b"Please provide map id (int), car id (int).\n")
                else:
                    map_id = int(args[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        _map = Repo._maps[map_id]
                        car_id = int(args[2])
                        if car_id in _map.cars:
                            _map.cars[car_id].stop()
                            self.socket.send(f"Car with {car_id} stopped.\n".encode())
                        else:
                            self.socket.send(f"Car with id {car_id} does not exist.\n".encode())
        elif args[0] == "ACCEL_CAR":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 3:
                    self.socket.send(b"Please provide map id (int), car id (int).\n")
                else:
                    map_id = int(args[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        _map = Repo._maps[map_id]
                        car_id = int(args[2])
                        if car_id in _map.cars:
                            try:
                                _map.cars[car_id].accel()
                                self.socket.send(f"Car with {car_id} accelerated.\n".encode())
                            except ValueError as e:
                                self.socket.send(str(e).encode())
                        else:
                            self.socket.send(f"Car with id {car_id} does not exist.\n".encode())
        elif args[0] == "BRAKE_CAR":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 3:
                    self.socket.send(b"Please provide map id (int), car id (int).\n")
                else:
                    map_id = int(args[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        _map = Repo._maps[map_id]
                        car_id = int(args[2])
                        if car_id in _map.cars:
                            try:
                                _map.cars[car_id].brake()
                                self.socket.send(f"Car with {car_id} braked.\n".encode())
                            except ValueError as e:
                                self.socket.send(str(e).encode())
                        else:
                            self.socket.send(f"Car with id {car_id} does not exist.\n".encode())
        elif args[0] == "LEFT_CAR":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 3:
                    self.socket.send(b"Please provide map id (int), car id (int).\n")
                else:
                    map_id = int(args[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        _map = Repo._maps[map_id]
                        car_id = int(args[2])
                        if car_id in _map.cars:
                            try:
                                _map.cars[car_id].left()
                                self.socket.send(f"Car with {car_id} turned left.\n".encode())
                            except ValueError as e:
                                self.socket.send(str(e).encode())
                        else:
                            self.socket.send(f"Car with id {car_id} does not exist.\n".encode())
        elif args[0] == "RIGHT_CAR":
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(args) != 3:
                    self.socket.send(b"Please provide map id (int), car id (int).\n")
                else:
                    map_id = int(args[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        _map = Repo._maps[map_id]
                        car_id = int(args[2])
                        if car_id in _map.cars:
                            try:
                                _map.cars[car_id].right()
                                self.socket.send(f"Car with {car_id} turned right.\n".encode())
                            except ValueError as e:
                                self.socket.send(str(e).encode())
                        else:
                            self.socket.send(f"Car with id {car_id} does not exist.\n".encode())
        else:
            self.socket.send(b"Unknown command.\n")



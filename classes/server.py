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
            self.process_command(message.decode().strip())
            message = self.socket.recv(1024)

    def process_command(self, command: str) -> None:
        if command.startswith("USER"):
            if len(command.split()) != 2:
                self.socket.send("Please provide a username.")
            else:
                self.username = command.split()[1]
                Repo.addUser(self.username)
                self.socket.send(f"Username set to {self.username}.\n".encode())
        elif command.startswith("ATTACH_MAP"):
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(command.split()) != 2:
                    self.socket.send(b"Please provide a map id.\n")
                else:
                    map_id = int(command.split()[1])
                    Repo.attach(map_id, self.username)
                    self.socket.send(f"Map {map_id} attached to user {self.username}.\n".encode())
        elif command.startswith("DETACH_MAP"):
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(command.split()) != 2:
                    self.socket.send(b"Please provide a map id.\n")
                else:
                    map_id = int(command.split()[1])
                    Repo.detach(map_id, self.username)
                    self.socket.send(f"Map {map_id} detached from user {self.username}.\n".encode())
        elif command.startswith("START_GAME"):
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(command.split()) != 2:
                    self.socket.send(b"Please provide a map id.\n")
                else:
                    map_id = int(command.split()[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        map = Repo.loadMap(map_id)
                        map.start()
                        self.socket.send(b"Game started.\n")
        elif command.startswith("STOP_GAME"):
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(command.split()) != 2:
                    self.socket.send(b"Please provide a map id.\n")
                else:
                    map_id = int(command.split()[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        Repo._maps[map_id].stop()
                        self.socket.send(b"Game stopped.\n")
        elif command.startswith("SAVE"):
            if self.username == "":
                self.socket.send(b"Please first enter your username with USER <username> command.\n")
            else:
                if len(command.split()) != 2:
                    self.socket.send(b"Please provide a map id.\n")
                else:
                    map_id = int(command.split()[1])
                    if map_id not in Repo._attached_maps[self.username]:
                        self.socket.send(b"Please attach the map first.\n")
                    else:
                        Repo.saveMap(map_id)
                        self.socket.send(b"Map saved.\n")
        else:
            self.socket.send(b"Unknown command.\n")



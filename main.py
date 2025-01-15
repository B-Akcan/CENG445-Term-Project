from classes.repo import Repo
import json
from websockets.sync.server import serve
from websockets import ConnectionClosedOK, ConnectionClosedError

username = ""

def handler(ws):
    print("Client connected")
    
    try:
        for msg in ws:
            print(msg)

            args = msg.split()
            if len(args) > 0:
                if args[0] == "USER":
                    if len(args) != 2:
                        ws.send("Please provide a username.")
                    else:
                        username = args[1]
                        Repo.addUser(username)
                        ws.send(f"Username set to {username}.")
                elif args[0] == "ATTACH_MAP":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 2:
                            ws.send("Please provide a map id.")
                        else:
                            map_id = int(args[1])
                            Repo.attach(map_id, username)
                            ws.send(f"Map {map_id} attached to user {username}.")
                elif args[0] == "DETACH_MAP":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 2:
                            ws.send("Please provide a map id.")
                        else:
                            map_id = int(args[1])
                            Repo.detach(map_id, username)
                            ws.send(f"Map {map_id} detached from user {username}.")
                elif args[0] == "START_GAME":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 2:
                            ws.send("Please provide a map id.")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                _map = Repo._maps[map_id]
                                _map.start()
                                ws.send("Game started.")
                elif args[0] == "STOP_GAME":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 2:
                            ws.send("Please provide a map id.")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                Repo.saveMap(map_id)
                                Repo._maps[map_id].stop()
                                ws.send("Game saved and stopped.")
                elif args[0] == "SAVE":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 2:
                            ws.send("Please provide a map id.")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                Repo.saveMap(map_id)
                                ws.send("Game saved.")
                elif args[0] == "CREATE_MAP":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 5:
                            ws.send("Please provide number of columns (int), number of rows (int), cellsize (int), background color (string).")
                        else:
                            cols, rows, cellsize = map(int, args[1:4])
                            bgcolor = args[4]
                            map_id = Repo.create(cols=cols, rows=rows, cellsize=cellsize, bgcolor=bgcolor)
                            Repo.attach(map_id, username)
                            ws.send(f"Map created with id {map_id} and attached to user {username}.")
                elif args[0] == "DELETE_MAP":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 2:
                            ws.send("Please provide map id.")
                        else:
                            map_id = int(args[1])
                            Repo.delete(map_id)
                            ws.send(f"Map with id {map_id} was detached from all users and deleted.")
                elif args[0] == "DRAW_MAP":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 2:
                            ws.send("Please provide map id.")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                _map = Repo._maps[map_id]
                                ws.send(_map.draw())
                elif args[0] == "REGISTER_COMP":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 2:
                            ws.send("Please provide component type.")
                        else:
                            comp = args[1]
                            try:
                                Repo().components.register(comp)
                                ws.send(f"Component {comp} registered.")
                            except ValueError as e:
                                ws.send(str(e))
                elif args[0] == "UNREGISTER_COMP":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 2:
                            ws.send("Please provide component type.")
                        else:
                            comp = args[1]
                            try:
                                Repo().components.unregister(comp)
                                ws.send(f"Component {comp} unregistered.")
                            except ValueError as e:
                                ws.send(str(e))
                elif args[0] == "REGISTER_ALL_COMPS":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        Repo().components.registerAll()
                        ws.send("All components registered.")
                elif args[0] == "GET_REGISTERED_COMPS":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        ws.send(json.dumps(Repo().components.registeredComponentsToList()))
                elif args[0] == "CREATE_COMP":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 5:
                            ws.send("Please provide map id (int), component type (str), x coordinate (int), y coordinate (int).")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                comp = args[2]
                                x, y = map(int, args[3:5])
                                _map = Repo._maps[map_id]
                                try:
                                    _map[(x, y)] = Repo().components.create(comp)
                                    ws.send(f"Component '{comp}' created at ({x},{y}).")
                                except ValueError as e:
                                    ws.send(str(e))
                                except IndexError as e:
                                    ws.send(str(e))
                elif args[0] == "ROTATE_COMP":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 4:
                            ws.send("Please provide map id (int), x coordinate (int), y coordinate (int).")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                x, y = map(int, args[2:4])
                                _map = Repo._maps[map_id]
                                try:
                                    _map[(x, y)].rotation = (_map[(x, y)].rotation + 1) % 4
                                    ws.send(f"Component at ({x},{y}) of map {map_id} was rotated.")
                                except ValueError as e:
                                    ws.send(str(e))
                                except IndexError as e:
                                    ws.send(str(e))
                elif args[0] == "DELETE_COMP":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 4:
                            ws.send("Please provide map id (int), x coordinate (int), y coordinate (int).")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                x, y = map(int, args[2:4])
                                _map = Repo._maps[map_id]
                                try:
                                    del _map[(x, y)]
                                    ws.send("Component deleted.")
                                except ValueError as e:
                                    ws.send(str(e))
                                except IndexError as e:
                                    ws.send(str(e))
                                except KeyError as e:
                                    ws.send((str(e).replace("'", "") + ""))
                elif args[0] == "CREATE_CAR":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 6:
                            ws.send("Please provide map id (int), model (str), driver (str), topspeed (int), topfuel (int).")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                try:
                                    model, driver = args[2:4]
                                    topspeed, topfuel = map(int, args[4:6])
                                    _map = Repo._maps[map_id]
                                    car = Repo().components.create("Car", model=model, map_ref=_map, driver=driver, topspeed=topspeed, topfuel=topfuel)
                                    _map.place(car, 0, 0)
                                    car_id = _map.get_car_id(car)
                                    ws.send(f"Created car with id {car_id}.")
                                except ValueError as e:
                                    ws.send(str(e))
                elif args[0] == "DELETE_CAR":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 3:
                            ws.send("Please provide map id (int), car id (int).")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                _map = Repo._maps[map_id]
                                car_id = int(args[2])
                                try:
                                    _map.remove_car(car_id)
                                    ws.send(f"Deleted car with id {car_id}.")
                                except KeyError as e:
                                    ws.send((str(e).replace("'", "") + ""))
                elif args[0] == "START_CAR":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 3:
                            ws.send("Please provide map id (int), car id (int).")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                _map = Repo._maps[map_id]
                                car_id = int(args[2])
                                if car_id in _map.cars:
                                    res = _map.start_car(car_id)
                                    ws.send(res)
                                else:
                                    ws.send(f"Car with id {car_id} does not exist.")
                elif args[0] == "STOP_CAR":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 3:
                            ws.send("Please provide map id (int), car id (int).")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                _map = Repo._maps[map_id]
                                car_id = int(args[2])
                                if car_id in _map.cars:
                                    res = _map.stop_car(car_id)
                                    ws.send(res)
                                else:
                                    ws.send(f"Car with id {car_id} does not exist.")
                elif args[0] == "ACCEL_CAR":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 3:
                            ws.send("Please provide map id (int), car id (int).")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                _map = Repo._maps[map_id]
                                car_id = int(args[2])
                                if car_id in _map.cars:
                                    res = _map.accel_car(car_id)
                                    ws.send(res)
                                else:
                                    ws.send(f"Car with id {car_id} does not exist.")
                elif args[0] == "BRAKE_CAR":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 3:
                            ws.send("Please provide map id (int), car id (int).")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                _map = Repo._maps[map_id]
                                car_id = int(args[2])
                                if car_id in _map.cars:
                                    res = _map.brake_car(car_id)
                                    ws.send(res)
                                else:
                                    ws.send(f"Car with id {car_id} does not exist.")
                elif args[0] == "LEFT_CAR":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 3:
                            ws.send("Please provide map id (int), car id (int).")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                _map = Repo._maps[map_id]
                                car_id = int(args[2])
                                if car_id in _map.cars:
                                    res = _map.left_car(car_id)
                                    ws.send(res)
                                else:
                                    ws.send(f"Car with id {car_id} does not exist.")
                elif args[0] == "RIGHT_CAR":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 3:
                            ws.send("Please provide map id (int), car id (int).")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                _map = Repo._maps[map_id]
                                car_id = int(args[2])
                                if car_id in _map.cars:
                                    res = _map.right_car(car_id)
                                    ws.send(res)
                                else:
                                    ws.send(f"Car with id {car_id} does not exist.")
                elif args[0] == "CAR_INFO":
                    if username == "":
                        ws.send("Please first enter your username with USER <username> command.")
                    else:
                        if len(args) != 3:
                            ws.send("Please provide map id (int), car id (int).")
                        else:
                            map_id = int(args[1])
                            if map_id not in Repo._attached_maps[username]:
                                ws.send("Please attach the map first.")
                            else:
                                _map = Repo._maps[map_id]
                                car_id = int(args[2])
                                if car_id in _map.cars:
                                    ws.send(json.dumps(_map.cars[car_id].get_car_info()))
                                else:
                                    ws.send(f"Car with id {car_id} does not exist.")
                else:
                    ws.send("Unknown command.")
    except ConnectionClosedOK:
        print("Client disconnected")
    except ConnectionClosedError:
        print("Connection closed with error")

if __name__ == "__main__":
    with serve(handler, "localhost", 8000) as server:
        server.serve_forever()
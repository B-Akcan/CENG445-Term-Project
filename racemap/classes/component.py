import math
import random
import time

class Component():
    _registered_components = {}

    def desc(self) -> str:
        return "Represents a component in the game"

    def type(self) -> str:
        return "Component"

    def attrs(self) -> dict:
        return {}

    def __getattr__(self, attr):
        if attr not in self.attrs():
            raise AttributeError(f"Class '{self.__class__.__name__}' has no attribute '{attr}'")
        super().__getattribute__(attr)

    def __setattr__(self, attr, value):
        if attr not in self.attrs():
            raise AttributeError(f"Class '{self.__class__.__name__}' has no attribute '{attr}'")
        super().__setattr__(attr, value)

    def draw(self) -> str:
        pass
    
    @classmethod
    def list(cls):
        print( [(name, comp.desc()) for name, comp in cls._registered_components.items()] )

    @classmethod
    def create(cls, component_type: str, *p, **kw):
        if component_type in cls._registered_components:
            return cls._registered_components[component_type](*p, **kw)
        raise ValueError(f"Component type '{component_type}' is not registered.\n")

    @classmethod
    def register(cls, component_type: str):
        if component_type == "Car":
            cls._registered_components[component_type] = Car
        elif component_type == "Cell":
            cls._registered_components[component_type] = Cell
        elif component_type == "Decoration":
            cls._registered_components[component_type] = Decoration
        elif component_type == "Checkpoint":
            cls._registered_components[component_type] = Checkpoint
        elif component_type == "Obstacle":
            cls._registered_components[component_type] = Obstacle
        elif component_type == "Wall":
            cls._registered_components[component_type] = Wall
        elif component_type == "Mud":
            cls._registered_components[component_type] = Mud
        elif component_type == "Ice":
            cls._registered_components[component_type] = Ice
        elif component_type == "Bonus":
            cls._registered_components[component_type] = Bonus
        elif component_type == "Booster":
            cls._registered_components[component_type] = Booster
        elif component_type == "Refuel":
            cls._registered_components[component_type] = Refuel
        elif component_type == "Road":
            cls._registered_components[component_type] = Road
        elif component_type == "StraightRoad":
            cls._registered_components[component_type] = StraightRoad
        elif component_type == "Turn90":
            cls._registered_components[component_type] = Turn90
        else:
            raise ValueError(f"{component_type} does not exist.\n")

    @classmethod
    def unregister(cls, component_type: str):
        if component_type in cls._registered_components:
            del cls._registered_components[component_type]
        else:
            raise ValueError(f"Component type '{component_type}' is already not registered.\n")
        
    @classmethod
    def registerAll(cls):
        comps = ["Car", "Cell", "Decoration", "Checkpoint", "Obstacle", "Wall", "Mud", "Ice", "Bonus", "Booster", "Refuel", "Road", "StraightRoad", "Turn90"]
        for c in comps:
            cls.register(c)

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

class Car(Component):
    def __init__(self, model, map_ref, driver, pos, angle, topspeed, topfuel):
        self.model = model
        self.map = map_ref # of type Map
        self.driver = driver
        self.pos = pos # (x, y)
        self.angle = angle
        self.topspeed = topspeed
        self.topfuel = topfuel
        self.speed = 0.0
        self.fuel = topfuel

        self.started = False
        self.accel_flag = False
        self.brake_flag = False
        self.left_flag = False
        self.right_flag = False

        self.lap_count = 0
        self.last_checkpoint = -1
        self.checkpoint_times = [None] * len(self.map.checkpoints)

    @classmethod
    def desc(cls) -> str:
        return "Represents a car in the game"

    @classmethod
    def type(cls) -> str:
        return "Car"

    @classmethod
    def attrs(cls) -> dict:
        return {
            "model": str,
            "map": object,
            "driver": str,
            "pos": (float, float),
            "angle": float,
            "topspeed": float,
            "topfuel": float,
            "speed": float,
            "fuel": float,
            "started": bool,
            "accel_flag": bool,
            "brake_flag": bool,
            "left_flag": bool,
            "right_flag": bool,
            "lap_count": int,
            "last_checkpoint": int,
            "checkpoint_times": [float]
        }

    def draw(self) -> str:
        return f"Car {self.model} with driver {self.driver} is at position ({self.pos[0]:.2f}, {self.pos[1]:.2f}) with speed {self.speed:.1f}, fuel {self.fuel:.2f} and angle {self.angle:.2f}."

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.started = False
        self.speed = 0.0
        self.accel_flag = False
        self.brake_flag = False
        self.left_flag = False
        self.right_flag = False

    def accel(self) -> None:
        if self.started:
            self.accel_flag = True
            return
        raise ValueError(f"Car '{self.model}' is not started.\n")

    def brake(self) -> None:
        if self.started:
            self.brake_flag = True
            return
        raise ValueError(f"Car '{self.model}' is not started.\n")

    def left(self) -> None:
        if self.started:
            self.left_flag = True
            return
        raise ValueError(f"Car '{self.model}' is not started.\n")

    def right(self) -> None:
        if self.started:
            self.right_flag = True
            return
        raise ValueError(f"Car '{self.model}' is not started.\n")

    def tick(self) -> None:
        if not self.started:
            print(f"Car '{self.model}' is not started")
            return
        if self.fuel <= 0:
            print(f"Car '{self.model}' is out of fuel")
            return

        # Set speed based on flags
        if self.accel_flag and self.speed < self.topspeed:
            self.speed += 3
        if self.brake_flag and self.speed > 0:
            self.speed -= 3

        # Set angle based on flags
        if self.left_flag:
            self.angle += 45
            if self.angle >= 360:
                self.angle -= 360
        if self.right_flag:
            self.angle -= 45
            if self.angle < 0:
                self.angle += 360

        # Update position based on speed and angle
        rad_angle = math.radians(self.angle)
        new_pos_x = self.pos[0] + self.speed * math.cos(rad_angle)
        new_pos_y = self.pos[1] - self.speed * math.sin(rad_angle)
        self.pos = (clamp(new_pos_x, 0, self.map.cols * self.map.cellsize),
                    clamp(new_pos_y, 0, self.map.rows * self.map.cellsize))

        # Reduce fuel based on speed
        self.fuel -= self.speed * 0.1
        if self.fuel < 0:
            self.fuel = 0

        # Interact with the current cell
        grid_pos = (int(self.pos[0] // self.map.cellsize), int(self.pos[1] // self.map.cellsize))
        try:
            cell = self.map[grid_pos]
        except:
            cell = None

        if cell and isinstance(cell, Cell):
            cell.interact(self, *self.pos)

        # Reset flags after processing
        self.accel_flag = False
        self.brake_flag = False
        self.left_flag = False
        self.right_flag = False

        print(f"{self.model} is at position ({self.pos[0]:.2f}, {self.pos[1]:.2f}) with speed {self.speed:.2f} and fuel {self.fuel:.2f}.")

    def to_dict(self): # excludes map_ref, to prevent circular reference
        return {
            "model": self.model,
            "driver": self.driver,
            "pos": self.pos,
            "angle": self.angle,
            "topspeed": self.topspeed,
            "topfuel": self.topfuel,
            "speed": self.speed,
            "fuel": self.fuel,
            "started": self.started,
            "accel_flag": self.accel_flag,
            "brake_flag": self.brake_flag,
            "left_flag": self.left_flag,
            "right_flag": self.right_flag,
        }
    
    def get_car_info(self) -> str:
        return f"Model: {self.model}, Driver: {self.driver}, Position: ({self.pos[0]:.2f},{self.pos[1]:.2f}), Angle: {self.angle}, Speed: {self.speed:.2f}, Fuel: {self.fuel:.2f}, Top Speed: {self.topspeed}, Top Fuel: {self.topfuel}, Is Started: {self.started}\n"
    
class Cell(Component):
    @classmethod
    def desc(cls) -> str:
        return "Represents a cell in the game"
    
    @classmethod
    def type(cls) -> str:
        return "Cell"

    @classmethod
    def attrs(cls) -> dict:
        return {
            "row": int,
            "col": int,
            "rotation": int
        }
    
    def draw(self) -> str:
        pass

    def interact(self, car, y, x):
        pass

    def to_dict(self):
        return {
            "row": self.row,
            "col": self.col,
            "rotation": self.rotation
        }
    
class Decoration(Cell):
    @classmethod
    def desc(cls) -> str:
        return "Represents a decoration cell in the game"
    
    @classmethod
    def type(cls) -> str:
        return "Decoration"
    
    def draw(self) -> str:
        return "D"
    
    def interact(self, car, y, x):
        # print("Car interacts with a decoration. No effect.")
        pass
    
class Checkpoint(Cell):
    @classmethod
    def desc(cls) -> str:
        return "Represents a checkpoint cell in the game"
    
    @classmethod
    def type(cls) -> str:
        return "Checkpoint"
    
    def draw(self) -> str:
        return "C"
    
    def interact(self, car, y, x):
        car_id = car.map.get_car_id(car)
        checkpoint_order = car.map.get_checkpoint_order(self)

        if car_id != -1:
            if (car.last_checkpoint + 1) % len(car.map.checkpoints) == checkpoint_order:
                prev_last_checkpoint = car.last_checkpoint
                car.last_checkpoint = checkpoint_order
                car.checkpoint_times[checkpoint_order] = time.time()
                if prev_last_checkpoint != -1 and checkpoint_order == 0:
                    car.lap_count += 1

    
class Obstacle(Cell):
    @classmethod
    def desc(cls) -> str:
        return "Represents a obstacle cell in the game"
    
    @classmethod
    def type(cls) -> str:
        return "Obstacle"
    
    def draw(self) -> str:
        pass
    
    def interact(self, car, y: float, x: float):
        pass

class Wall(Obstacle):
    @classmethod
    def desc(cls) -> str:
        return "Represents a wall obstacle cell in the game"
    
    @classmethod
    def type(cls) -> str:
        return "Wall"
    
    def draw(self) -> str:
        return "W"
    
    def interact(self, car, y: float, x: float):
        car.speed = 0

class Mud(Obstacle):
    @classmethod
    def desc(cls) -> str:
        return "Represents a mud obstacle cell in the game"
    
    @classmethod
    def type(cls) -> str:
        return "Mud"
    
    def draw(self) -> str:
        return "M"
    
    def interact(self, car, y: float, x: float):
        car.speed = max(0, car.speed - 5)

class Ice(Obstacle):
    @classmethod
    def desc(cls) -> str:
        return "Represents a ice obstacle cell in the game"
    
    @classmethod
    def type(cls) -> str:
        return "Ice"
    
    def draw(self) -> str:
        return "I"
    
    def interact(self, car, y: float, x: float):
        car.angle = random.randint(0, 359)

class Bonus(Cell):
    @classmethod
    def desc(cls) -> str:
        return "Represents a bonus cell in the game"
    
    @classmethod
    def type(cls) -> str:
        return "Bonus"
    
    def draw(self) -> str:
        pass
    
    def interact(self, car, y: float, x: float):
        pass
    
class Booster(Bonus):
    @classmethod
    def desc(cls) -> str:
        return "Represents a booster bonus cell in the game"
    
    @classmethod
    def type(cls) -> str:
        return "Booster"
    
    def draw(self) -> str:
        return "B"
    
    def interact(self, car, y: float, x: float):
        car.speed = min(car.topspeed, car.speed + 5)

class Refuel(Bonus):
    @classmethod
    def desc(cls) -> str:
        return "Represents a refuel bonus cell in the game"
    
    @classmethod
    def type(cls) -> str:
        return "Refuel"
    
    def draw(self) -> str:
        return "R"
    
    def interact(self, car, y: float, x: float):
        car.fuel = min(car.topfuel, car.fuel + 5)
    
class Road(Cell):
    @classmethod
    def desc(cls) -> str:
        return "Represents a road cell in the game"
    
    @classmethod
    def type(cls) -> str:
        return "Road"
    
    def draw(self) -> str:
        pass
    
    def interact(self, car, y, x):
        car.speed = max(0, car.speed - 0.01)  # due to friction
    
class StraightRoad(Road):
    @classmethod
    def desc(cls) -> str:
        return "Represents a straight road cell in the game"
    
    @classmethod
    def type(cls) -> str:
        return "StraightRoad"
    
    def draw(self) -> str:
        if self.rotation == 0:
            return "━"
        elif self.rotation == 1:
            return "┃"
        elif self.rotation == 2:
            return "╲"
        else:
            return "╱"
    
class Turn90(Road):
    @classmethod
    def desc(cls) -> str:
        return "Represents a turn90 road cell in the game"
    
    @classmethod
    def type(cls) -> str:
        return "Turn90"
    
    def draw(self) -> str:
        if self.rotation == 0:
            return "┏"
        elif self.rotation == 1:
            return "┓"
        elif self.rotation == 2:
            return "┛"
        else:
            return "┗"
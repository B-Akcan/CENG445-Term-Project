from .component import Component
from .map import Map
import math
from .cell import Cell

class Car(Component):
    def __init__(self, model: str = "", map_ref: Map | None = None, driver: str = "", pos: tuple[float, float] = (0.0, 0.0),
                 angle: float = 0.0, topspeed: float = 100.0, topfuel: float = 100.0):
        self.model = model
        self.map = map_ref
        self.driver = driver
        self.pos = pos
        self.angle = angle
        self.topspeed = topspeed
        self.topfuel = topfuel
        self.speed = 0.0
        self.fuel = topfuel

        self.active = False  # Track whether the car is started
        self.accel_flag = False
        self.brake_flag = False
        self.left_flag = False
        self.right_flag = False

    def desc(self) -> str:
        "An instance of Car class"

    def type(self) -> str:
        "Car"

    def attrs(self) -> dict:
        return {
            "model": self.model,
            "driver": self.driver,
            "pos": self.pos,
            "angle": self.angle,
            "topspeed": self.topspeed,
            "topfuel": self.topfuel,
            "speed": self.speed,
            "fuel": self.fuel
        }

    def draw(self) -> str:
        pass

    def start(self) -> None:
        self.active = True

    def stop(self) -> None:
        self.active = False
        self.speed = 0.0
        self.accel_flag = False
        self.brake_flag = False
        self.left_flag = False
        self.right_flag = False

    def accel(self) -> None:
        if self.active:
            self.accel_flag = True

    def brake(self) -> None:
        if self.active:
            self.brake_flag = True

    def left(self) -> None:
        if self.active:
            self.left_flag = True

    def right(self) -> None:
        if self.active:
            self.right_flag = True

    def tick(self) -> None:
        if not self.active:
            print(f"Car {self.model} is not started")
            return
        if self.fuel <= 0:
            print(f"Car {self.model} is out of fuel")
            return

        # Set speed based on flags
        if self.accel_flag and self.speed < self.topspeed:
            self.speed += 1
        if self.brake_flag and self.speed > 0:
            self.speed -= 1

        # Set angle based on flags
        if self.left_flag:
            self.angle -= 5
        if self.right_flag:
            self.angle += 5

        # Update position based on speed and angle
        rad_angle = math.radians(self.angle)
        self.pos = (self.pos[0] + self.speed * math.sin(rad_angle),
                    self.pos[1] + self.speed * math.cos(rad_angle))

        # Reduce fuel based on speed
        self.fuel -= self.speed * 0.1
        if self.fuel < 0:
            self.fuel = 0

        # Interact with the current cell
        grid_pos = (int(self.pos[0] // self.map.cellsize), int(self.pos[1] // self.map.cellsize))
        component = self.map[grid_pos] if (0 <= grid_pos[0] < self.map.rows and 0 <= grid_pos[1] < self.map.cols) else None

        if component and isinstance(component, Cell):
            component.interact(self, *self.pos)

        # Reset flags after processing
        self.accel_flag = False
        self.brake_flag = False
        self.left_flag = False
        self.right_flag = False

        print(f"{self.model} is at position {self.pos} with speed {self.speed} and fuel {self.fuel}.")
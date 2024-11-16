from .component import Component
import math
from .cell import Cell
from .map import Map

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

class Car(Component):
    def __init__(self, model, map_ref, driver, pos, angle, topspeed, topfuel):
        self.model = model
        self.map = map_ref
        self.driver = driver
        self.pos = pos
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
            "map": Map,
            "driver": str,
            "pos": tuple[float, float],
            "angle": float,
            "topspeed": float,
            "topfuel": float,
            "speed": float,
            "fuel": float,
            "started": bool,
            "accel_flag": bool,
            "brake_flag": bool,
            "left_flag": bool,
            "right_flag": bool
        }

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
        else:
            print(f"Car '{self.model}' is not started")

    def brake(self) -> None:
        if self.started:
            self.brake_flag = True
        else:
            print(f"Car '{self.model}' is not started")

    def left(self) -> None:
        if self.started:
            self.left_flag = True
        else:
            print(f"Car '{self.model}' is not started")

    def right(self) -> None:
        if self.started:
            self.right_flag = True
        else:
            print(f"Car '{self.model}' is not started")

    def tick(self) -> None:
        if not self.started:
            print(f"Car '{self.model}' is not started")
            return
        if self.fuel <= 0:
            print(f"Car '{self.model}' is out of fuel")
            return

        # Set speed based on flags
        if self.accel_flag and self.speed < self.topspeed:
            self.speed += 1
        if self.brake_flag and self.speed > 0:
            self.speed -= 1

        # Set angle based on flags
        if self.left_flag:
            self.angle += 45
        if self.right_flag:
            self.angle -= 45

        # Update position based on speed and angle
        rad_angle = math.radians(self.angle)
        new_pos_x = self.pos[0] + self.speed * math.sin(rad_angle)
        new_pos_y = self.pos[1] + self.speed * math.cos(rad_angle)
        self.pos = (clamp(new_pos_x, 0, self.map.cols * self.map.cellsize),
                    clamp(new_pos_y, 0, self.map.rows * self.map.cellsize))

        # Reduce fuel based on speed
        self.fuel -= self.speed * 0.1
        if self.fuel < 0:
            self.fuel = 0

        # Interact with the current cell
        grid_pos = (int(self.pos[0] // self.map.cellsize), int(self.pos[1] // self.map.cellsize))
        cell = self.map[grid_pos] if (0 <= grid_pos[0] < self.map.rows and 0 <= grid_pos[1] < self.map.cols) else None

        if cell and isinstance(cell, Cell):
            cell.interact(self, *self.pos)

        # Reset flags after processing
        self.accel_flag = False
        self.brake_flag = False
        self.left_flag = False
        self.right_flag = False

        print(f"{self.model} is at position {self.pos} with speed {self.speed} and fuel {self.fuel}.")
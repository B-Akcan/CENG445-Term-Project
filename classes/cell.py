from .component import Component
import random

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
        print("Car interacts with a decoration. No effect.")
    
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
        print(f"Car {car.model} reached a checkpoint at ({x}, {y}).")
    
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
        car.speed = max(0, car.speed - 3)

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
        car.speed = min(car.topspeed, car.speed + 3)

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
        car.speed = max(0, car.speed - 0.5)  # due to friction
    
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
    
from .component import Component

class Cell(Component):
    def __init__(self, row, col, rotation):
        self.row = row
        self.col = col
        self.rotation = rotation

    def interact(self, car, y, x): # Abstract method, will be overridden
        pass

    def type(self) -> str:
        return "Cell"

    def attrs(self) -> dict:
        return {"row": int, "col": int, "rotation": int}
    
class Decoration(Cell):
    def type(self) -> str:
        return "Decoration"
    
class Checkpoint(Cell):
    def type(self) -> str:
        return "Checkpoint"
    
class Obstacle(Cell):
    def type(self) -> str:
        return "Obstacle"
    
    def interact(self, car, y: float, x: float):
        car.speed = 0
    
class Booster(Cell):
    def type(self) -> str:
        return "Booster"
    
    def interact(self, car, y: float, x: float):
        car.speed = min(car.topspeed, car.speed + 5)

class Refuel(Cell):
    def type(self) -> str:
        return "Refuel"
    
    def interact(self, car, y: float, x: float):
        car.fuel = min(car.topfuel, car.fuel + 20)
    
class Road(Cell):
    def type(self) -> str:
        return "Road"
    
    def interact(self, car, y: float, x: float):
        car.speed = max(0, car.speed - 0.5)  # due to friction
    
class StraightRoad(Road):
    def type(self) -> str:
        return "StraightRoad"
    
class StraightAxisAlignedRoad(StraightRoad):
    def type(self) -> str:
        return "StraightAxisAlignedRoad"
    
class StraightDiagonalRoad(StraightRoad):
    def type(self) -> str:
        return "StraightDiagonalRoad"
    
class TurningRoad(Road):
    def type(self) -> str:
        return "TurningRoad"
    
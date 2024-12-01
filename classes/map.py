from .cell import Cell, Checkpoint
from .singleton import Singleton
import threading as th
import time

class CarIdCounter(Singleton):
    val = 0

    def get(self):
        cur = self.val
        self.val += 1
        return cur
    
class CheckpointIdCounter(Singleton):
    val = 0

    def get(self):
        cur = self.val
        self.val += 1
        return cur

class Map():
    def __init__(self, cols: int, rows: int, cellsize: int, bgcolor: str):
        self.cols: int = cols
        self.rows: int = rows
        self.cellsize: int = cellsize
        self.bgcolor: str = bgcolor
        self.grid: list[list[Cell]] = [[None for _ in range(cols)] for _ in range(rows)]
        self.cars = {}  # dict[int(car id), Car]
        self.checkpoints: dict[int, Checkpoint] = {} # dict[int(checkpoint id), Checkpoint]
        self.lap_counts: dict[int, int] = {}  # dict[int(Car id), int(lap count)]
        self.last_checkpoints: dict[int, int] = {} # dict[int(Car id), int(last checkpoint id)]
        self.checkpoint_times: dict[int, list[float]] = {} # dict[int(Car id), list[float]]
        self.game_mode: bool = False
        self.lock: th.Lock = th.Lock()

    def __getitem__(self, pos: tuple[int, int]): # Get the cell at given position
        row, col = pos
        try:
            return self.grid[row][col]
        except IndexError:
            print("Position out of map bounds")

    def __setitem__(self, pos: tuple[int, int], cell: Cell): # Place a cell at given position
        row, col = pos
        try:
            self.grid[row][col] = cell
            cell.row = row
            cell.col = col
            cell.rotation = 0

            if isinstance(cell, Checkpoint):
                self.add_checkpoint(cell)
        except IndexError:
            print("Position out of map bounds")

    def __delitem__(self, pos: tuple[int, int]): # Remove the cell at given position
        row, col = pos
        try:
            cell = self.grid[row][col]
            self.grid[row][col] = None

            if isinstance(cell, Checkpoint):
                self.remove_checkpoint(cell)
        except IndexError:
            print("Position out of map bounds")

    def removeAllCellsWithType(self, cell_type: str): # Remove all cells of a given type from the map
        for row in range(self.rows):
            for col in range(self.cols):
                if type(self.grid[row][col]) == cell_type:
                    self.grid[row][col] = None

    def getxy(self, x: int, y: int): # Get the component based on pixel position
        row = y // self.cellsize
        col = x // self.cellsize
        return self.grid[row][col]

    def place(self, obj, x, y): # Place a component at a pixel position
        row = y // self.cellsize
        col = x // self.cellsize

        if isinstance(obj, Cell):
            self.grid[row][col] = obj
            obj.row = row
            obj.col = col
            obj.rotation = 0

            if isinstance(obj, Checkpoint):
                self.add_checkpoint(obj)

        elif obj.__class__.__name__ == "Car":
            obj.pos = (x, y)
            self.add_car(obj)

    def view(self, x, y, width, height): # Return a view (subsection) of the map with given width and height
        view_map = Map(height, width, self.cellsize, self.bgcolor)
        for row in range(view_map.rows):
            for col in range(view_map.cols):
                view_map.grid[row][col] = self.grid[row + x][col + y]

        return view_map

    def add_car(self, car) -> None:
        with self.lock:
            if car not in list(self.cars.values()):
                car_id = CarIdCounter().get()
                self.cars[car_id] = car
                self.lap_counts[car_id] = 0
                self.last_checkpoints[car_id] = -1
    
    def remove_car(self, car) -> None:
        with self.lock:
            car_id = -1
            for k in self.cars:
                if self.cars[k] == car:
                    car_id = k

            if car_id != -1:
                del self.cars[car_id]
                del self.lap_counts[car_id]
                del self.last_checkpoints[car_id]

    def get_car_id(self, car) -> int:
        for k in self.cars:
            if self.cars[k] == car:
                return k
        return -1

    def add_checkpoint(self, checkpoint: Checkpoint) -> None:
        with self.lock:
            checkpoint_id = CheckpointIdCounter().get()
            self.checkpoints[checkpoint_id] = checkpoint

    def remove_checkpoint(self, checkpoint: Checkpoint) -> None:
        with self.lock:
            cp_id = -1
            for k in self.checkpoints:
                if self.checkpoints[k] == checkpoint:
                    cp_id = k

            if cp_id != -1:
                del self.checkpoints[cp_id]

    def get_checkpoint_id(self, checkpoint: Checkpoint) -> int:
        for k in self.checkpoints:
            if self.checkpoints[k] == checkpoint:
                return k
        return -1

    def draw(self) -> None:
        """Sort cars by laps and last visited checkpoints.
            Draw the map on the command line.
            Print ordered car laps, last checkpoint, time elapsed."""
        
        with self.lock:
            car_ids = self.sort_cars()

            for row in range(self.rows):
                for col in range(self.cols):
                    cell = self.grid[row][col]
                    if cell:
                        print(cell.draw(), end="")
                    else:
                        print(".", end="")
                print(end="\n")

            print("Car Rankings:")
            for i in car_ids:
                car = self.cars[i]
                lap_count = self.lap_counts[i]
                checkpoint = self.last_checkpoints[i]
                if checkpoint != -1:
                    time_elapsed = self.checkpoint_times[i][checkpoint]
                    print(f"{car.model}: {lap_count} laps, last checkpoint: {checkpoint}, time elapsed since last checkpoint: {time_elapsed:.2f} s")
                else:
                    print(f"{car.model}: {lap_count} laps, last checkpoint: None")

    def sort_cars(self) -> list[int]:
        sorted_lap_counts = dict(sorted(self.lap_counts.items(), key=lambda x: x[1], reverse=True)) # sort by descending lap counts
        car_ids = list(sorted_lap_counts.keys())

        # Sort by descending last checkpoints
        swapped = True
        while swapped:
            swapped = False
            i = 0
            while i < len(car_ids) - 1:
                if self.lap_counts[car_ids[i]] == self.lap_counts[car_ids[i+1]] and self.last_checkpoints[car_ids[i]] < self.last_checkpoints[car_ids[i+1]]:
                    car_ids[i], car_ids[i+1] = car_ids[i+1], car_ids[i]
                    swapped = True
                i += 1
        
        return car_ids
                
    def start(self) -> None:
        if not self.game_mode: 
            self.game_mode = True
            self.start_time = time.time()
            game_thread = th.Thread(target=self.game_loop)
            game_thread.start()

    def stop(self) -> None:
        self.game_mode = False

    def game_loop(self) -> None:
        tick_interval = 0.1
        while self.game_mode:
            with self.lock:
                for car_id in self.cars:
                    self.cars[car_id].tick()
            time.sleep(tick_interval)

    def to_dict(self):
        return {
            "cols": self.cols,
            "rows": self.rows,
            "cellsize": self.cellsize,
            "bgcolor": self.bgcolor,
            "grid": [[cell.to_dict() if cell else None for cell in row] for row in self.grid],
            "cars": {car_id: car.to_dict() for car_id, car in self.cars.items()},
            "checkpoints": {checkpoint_id: checkpoint.to_dict() for checkpoint_id, checkpoint in self.checkpoints.items()},
            "lap_counts": self.lap_counts,
            "last_checkpoints": self.last_checkpoints,
            "checkpoint_times": self.checkpoint_times,
            "game_mode": self.game_mode,
            "start_time": self.start_time
        }

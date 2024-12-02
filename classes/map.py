from .singleton import Singleton
from .component import Cell, Checkpoint, Car
import threading as th
import time

class ComponentIdCounter(Singleton):
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
        self.game_mode: bool = False
        self.start_time = 0.0
        self.lock: th.Lock = th.Lock()

        self.grid: list[list[Cell]] = [[None for _ in range(cols)] for _ in range(rows)]
        self.cells: dict[int, Cell] = {} # dict[int(cell id), Cell]
        self.cars: dict[int, Car] = {}  # dict[int(car id), Car]
        self.checkpoints: dict[int, Checkpoint] = {} # dict[int(checkpoint id), Checkpoint]

    def __getitem__(self, pos): # Get the cell at given position
        row, col = pos
        if 0 <= row < self.rows or 0 <= col < self.cols:
            return self.grid[row][col]
        raise IndexError("Position out of map bounds\n")

    def __setitem__(self, pos, cell: Cell): # Place a cell at given position
        row, col = pos
        if 0 <= row < self.rows or 0 <= col < self.cols:
            self.grid[row][col] = cell
            cell.row = row
            cell.col = col
            cell.rotation = 0

            self.add_cell(cell)
            
            return
        
        raise IndexError("Position out of map bounds\n")

    def __delitem__(self, pos): # Remove the cell at given position
        row, col = pos
        if 0 <= row < self.rows or 0 <= col < self.cols:
            cell = self.grid[row][col]
            self.grid[row][col] = None

            cell_id = self.get_cell_id(cell)
            self.remove_cell(cell_id)

            return
        
        raise IndexError("Position out of map bounds\n")

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

            self.add_cell(obj)

        elif obj.__class__.__name__ == "Car":
            obj.pos = (x, y)
            return self.add_car(obj)
            
    def view(self, x, y, width, height): # Return a view (subsection) of the map with given width and height
        view_map = Map(height, width, self.cellsize, self.bgcolor)
        for row in range(view_map.rows):
            for col in range(view_map.cols):
                view_map.grid[row][col] = self.grid[row + x][col + y]

        return view_map
    
    def add_cell(self, cell) -> None:
        with self.lock:
            if cell not in list(self.cells.values()):
                cell_id = ComponentIdCounter().get()
                self.cells[cell_id] = cell

                if isinstance(cell, Checkpoint):
                    self.checkpoints[cell_id] = cell

                return cell_id
            return -1
        
    def remove_cell(self, cell_id: int) -> None:
        with self.lock:
            cell = self.cells[cell_id]

            if isinstance(cell, Checkpoint):
                for c in self.checkpoints:
                    if self.checkpoints[c] == cell:
                        del self.checkpoints[c]
                        break

            del self.cells[cell_id]

    def get_cell_id(self, cell: Cell) -> int:
        for c in self.cells:
            if self.cells[c] == cell:
                return c
        return -1
            
    def add_car(self, car) -> None:
        with self.lock:
            if car not in list(self.cars.values()):
                car_id = ComponentIdCounter().get()
                self.cars[car_id] = car
                return car_id
            return -1
    
    def remove_car(self, car_id: int) -> None:
        with self.lock:
            del self.cars[car_id]

    def get_car_id(self, car) -> int:
        for k in self.cars:
            if self.cars[k] == car:
                return k
        return -1
    
    def get_checkpoint_order(self, checkpoint: Checkpoint) -> int:
        i = 0
        cps = list(self.checkpoints.values())
        while i < len(cps):
            if cps[i] == checkpoint:
                return i
            i += 1
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
                checkpoint = car.last_checkpoint
                if checkpoint != -1:
                    time_elapsed = time.time() - car.checkpoint_times[checkpoint]
                    print(f"{car.model}: {car.lap_count} lap(s), last checkpoint: {checkpoint}, time elapsed since last checkpoint: {time_elapsed:.2f} s")
                else:
                    print(f"{car.model}: {car.lap_count} lap(s), last checkpoint: None")

    def sort_cars(self):
        len_cars = len(self.cars)
        car_ids = list(self.cars.keys())
        cars = list(self.cars.values())

        # sort by descending lap counts
        swapped = True
        while swapped:
            swapped = False
            i = 0
            while i < len_cars - 1:
                if cars[i].lap_count < cars[i+1].lap_count:
                    cars[i], cars[i+1] = cars[i+1], cars[i]
                    car_ids[i], car_ids[i+1] = car_ids[i+1], car_ids[i]
                    swapped = True
                i += 1

        # sort by descending last checkpoints
        swapped = True
        while swapped:
            swapped = False
            i = 0
            while i < len_cars - 1:
                if cars[i].lap_count == cars[i+1].lap_count and cars[i].last_checkpoint < cars[i+1].last_checkpoint:
                    cars[i], cars[i+1] = cars[i+1], cars[i]
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
        self.start_time = 0.0

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
            "game_mode": self.game_mode,
            "start_time": self.start_time,
            "grid": [[cell.to_dict() if cell else None for cell in row] for row in self.grid],
            "cells": {cell_id: cell.to_dict() for cell_id, cell in self.cells.items()},
            "cars": {car_id: car.to_dict() for car_id, car in self.cars.items()},
            "checkpoints": {checkpoint_id: checkpoint.to_dict() for checkpoint_id, checkpoint in self.checkpoints.items()}
        }

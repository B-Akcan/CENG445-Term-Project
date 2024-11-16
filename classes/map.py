from .component import Component
from .cell import Cell

class Map():
    def __init__(self, cols: int, rows: int, cellsize: int, bgcolor: str):
        self.cols = cols
        self.rows = rows
        self.cellsize = cellsize
        self.bgcolor = bgcolor
        self.grid: list[list[Cell]] = [[None for _ in range(cols)] for _ in range(rows)]

    def draw(self) -> None:
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if cell:
                    print(cell.draw(), end="")
                else:
                    print(".", end="")
            print(end="\n")

    def __getitem__(self, pos: tuple[int, int]): # Get the cell at (row, col) position
        row, col = pos
        try:
            return self.grid[row][col]
        except IndexError:
            print("Position out of map bounds")

    def __setitem__(self, pos: tuple[int, int], cell: Cell): # Place a cell at (row, col) position
        row, col = pos
        try:
            self.grid[row][col] = cell
        except IndexError:
            print("Position out of map bounds")

    def __delitem__(self, pos: tuple[int, int]): # Remove the cell at (row, col) position
        row, col = pos
        try:
            self.grid[row][col] = None
        except IndexError:
            print("Position out of map bounds")

    def remove(self, cell: Cell): # Remove a specific cell from the map
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == cell:
                    self.grid[row][col] = None

    def getxy(self, y: int, x: int): # Get the component based on pixel position
        row = y // self.cellsize
        col = x // self.cellsize
        return self.grid[row][col]

    def place(self, obj, y, x): # Place a component at a pixel position
        row = y // self.cellsize
        col = x // self.cellsize
        self.grid[row][col] = obj

    def view(self, y, x, height, width): # Return a view (subsection) of the map with given width and height
        view_map = Map(height, width, self.cellsize, self.bgcolor)
        for row in range(view_map.rows):
            for col in range(view_map.cols):
                view_map.grid[row][col] = self.grid[row + x][col + y]

        return view_map


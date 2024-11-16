from .cell import Cell

class Map():
    def __init__(self, cols: int, rows: int, cellsize: int, bgcolor: str):
        self.cols = cols
        self.rows = rows
        self.cellsize = cellsize
        self.bgcolor = bgcolor
        self.grid: list[list[Cell]] = [[None for _ in range(cols)] for _ in range(rows)]
        # self.cars = []

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
        except IndexError:
            print("Position out of map bounds")

    def __delitem__(self, pos: tuple[int, int]): # Remove the cell at given position
        row, col = pos
        try:
            self.grid[row][col] = None
        except IndexError:
            print("Position out of map bounds")

    def remove(self, cell: Cell): # Remove all cells of a given type from the map
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

        if obj.__class__.__name__ == "Cell":
            self.grid[row][col] = obj
            obj.row = row
            obj.col = col
        elif obj.__class__.__name__ == "Car":
            obj.pos = (x, y)
            # self.cars.append(obj)

    def view(self, y, x, height, width): # Return a view (subsection) of the map with given width and height
        view_map = Map(height, width, self.cellsize, self.bgcolor)
        for row in range(view_map.rows):
            for col in range(view_map.cols):
                view_map.grid[row][col] = self.grid[row + x][col + y]

        return view_map
    
    def draw(self) -> None: # Draw the map in command line
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if cell:
                    print(cell.draw(), end="")
                else:
                    print(".", end="")
            print(end="\n")

        # for car in self.cars:
        #     car.draw()


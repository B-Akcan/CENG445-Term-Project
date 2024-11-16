from .component import Component

class Map:
    def __init__(self, cols, rows, cellsize, bgcolor):
        self.cols = cols
        self.rows = rows
        self.cellsize = cellsize
        self.bgcolor = bgcolor
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    def __getitem__(self, pos: tuple[int, int]): # Get the component at (row, col) position
        row, col = pos

        try:
            return self.grid[row][col]
        except IndexError:
            print("Position out of map bounds")

    def __setitem__(self, pos: tuple[int, int], component: Component): # Place a component at (row, col) position
        row, col = pos

        try:
            self.grid[row][col] = component
        except IndexError:
            print("Position out of map bounds")

    def __delitem__(self, pos: tuple[int, int]): # Remove the component at (row, col) position
        row, col = pos

        try:
            self.grid[row][col] = None
        except IndexError:
            print("Position out of map bounds")

    def remove(self, component: Component): # Remove a specific component from the map
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == component:
                    self.grid[row][col] = None

    def getxy(self, y: int, x: int): # Get the component based on pixel position
        row = y // self.cellsize
        col = x // self.cellsize
        return self[row, col]

    def place(self, obj, y, x): # Place a car (or any component) at a pixel position
        row = y // self.cellsize
        col = x // self.cellsize
        self[row, col] = obj

    def view(self, y, x, height, width): # Return a view (subsection) of the map with given width and height
        start_row = max(0, y // self.cellsize)
        start_col = max(0, x // self.cellsize)
        end_row = min(self.rows, start_row + height // self.cellsize)
        end_col = min(self.cols, start_col + width // self.cellsize)

        view_map = Map(end_col - start_col, end_row - start_row, self.cellsize, self.bgcolor)
        for row in range(view_map.rows):
            for col in range(view_map.cols):
                view_map[row, col] = self[start_row + row, start_col + col]

        return view_map

    def draw(self) -> str: # Simple visual representation of the map grid in the console
        for row in self.grid:
            print(" ".join([cell.type()[0] if cell else '.' for cell in row]))


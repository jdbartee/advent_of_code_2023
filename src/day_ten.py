from .aoc_lib import Solution

RIGHT = (1, 0)
DOWN = (0, 1)
UP = (0, -1)
LEFT = (-1, 0)

class Point:
    def __init__(self, x:int, y:int):
        self.x = x
        self.y = y
        self.targets = []

    def plus(self, dx:int, dy:int):
        return self.x+dx, self.y+dy
    
    def exits_up(self) -> bool:
        if self.plus(*UP) in self.targets:
            return True


class Grid:

    _mapping = {
      '|': [UP, DOWN],
      '-': [LEFT, RIGHT],
      'F': [RIGHT, DOWN],
      'J': [LEFT, UP],
      '7': [LEFT, DOWN],
      'L': [UP, RIGHT],
      '.': [],
      'S': [],  
    }

    def __init__(self, width, height) -> None:
        self.height = height
        self.width = width
        self.points = [[Point(x,y) for x in range(width)] for y in range(height)]
        self.start = None

    def get_point(self, x, y) -> Point:
        return self.points[y][x]

    def point_valid(self, x, y):
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    def insert(self, x: int, y: int, glyph: str):
        if not self.point_valid(x, y):
            return
        
        if glyph == 'S':
            self.start = self.get_point(x, y)
            return
        
        point = self.get_point(x, y)
        offsets = self._mapping[glyph]
        for offest in offsets:
            target = point.plus(*offest)
            if self.point_valid(*target):
                point.targets.append(target)

    def update_start(self):
        for offset in [UP, DOWN, LEFT, RIGHT]:
            other = self.start.plus(*offset)
            if self.point_valid(*other):
                other_point = self.get_point(*other)
                if (self.start.x, self.start.y) in other_point.targets:
                    self.start.targets.append(other)

    @classmethod
    def load_from_str(cls, text: str):
        size = get_size(text)
        grid = Grid(*size)
        for y, line in enumerate(text.splitlines()):
            for x, glyph in enumerate(line):
                grid.insert(x, y, glyph)
        grid.update_start()
        return grid



class PathNode:
    def __init__(self) -> None:
        self.previous = None
        self.current = None
        self.length = None

    def next_node(self, grid: Grid):
        next_node = PathNode()
        next_node.previous = self.current
        point = grid.get_point(*self.current)
        for target in point.targets:
            if target != self.previous:
                next_node.current = target
                next_node.length = self.length + 1


                return next_node
        return None
    
    @classmethod
    def starting_pair(self, grid: Grid):
        starts = []
        for target in grid.start.targets:
            node = PathNode()
            node.previous = (grid.start.x, grid.start.y)
            node.current = target
            node.length = 1
            starts.append(node)
        return starts
    
    def print(self):
        print(f"L: {self.length} | P: {self.previous} | C: {self.length}")

    
class Loop:
    def __init__(self, width, height) -> None:
        self.height = height
        self.width = width
        self.up_loop_points = set()
        self.other_loop_points = set()


    def add_to_loop(self, grid: Grid, x, y) -> bool:
        vert = (x,y)
        if vert in self.up_loop_points or vert in self.other_loop_points:
            return False
        

        point = grid.get_point(*vert)
        if point.exits_up():
            self.up_loop_points.add(vert)
        else:
            self.other_loop_points.add(vert)
        
        return True
    
    def count_inner_cells(self):
        count = 0
        for y in range(self.height):
            inside_loop = False
            for x in range(self.width):
                vert = (x,y)
                if vert in self.up_loop_points:
                    inside_loop = not inside_loop
                elif vert in self.other_loop_points:
                    ...
                elif inside_loop:
                    count += 1
                else:
                    ...
        return count
                    

    def print_loop(self):
        for y in range(self.height):
            line = ""
            for x in range(self.width):
                if (x,y) in self.up_loop_points:
                    line = line+'|'
                elif (x,y) in self.other_loop_points:
                    line = line+'-'
                else:
                    line = line +'.'
            print(line)

def get_size(text:str):
    lines = text.splitlines()
    return len(lines[0]), len(lines)

class DayTen(Solution):
    command_name = 'd10'

    def part_one(self):
        grid = Grid.load_from_str(self.input_data)
        paths = PathNode.starting_pair(grid)
        if len(paths) != 2:
            raise "Assumptions Invalid"

        while paths[0].current != paths[1].current:
            paths[0] = paths[0].next_node(grid)
            paths[1] = paths[1].next_node(grid)
        
        return paths[0].length

    def part_two(self):
        grid = Grid.load_from_str(self.input_data)
        paths = PathNode.starting_pair(grid)
        path = paths[0]
        loop = Loop(grid.width, grid.height)
        while loop.add_to_loop(grid, *path.current):
            path = path.next_node(grid)
        
        return loop.count_inner_cells()
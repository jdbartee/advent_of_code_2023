from collections import namedtuple
from typing import List, Set, Tuple
from .aoc_lib import Solution, ColoredString, TerminalColor
from functools import lru_cache

Point = namedtuple('Point', ['y', 'x'])

class Diretion:
    NORTH: Point = Point(-1,0)
    SOUTH: Point =Point(1,0)
    EAST: Point = Point(0,1)
    WEST: Point = Point(0,-1)

    @staticmethod
    def valid(p: Point):
        return p in [Diretion.NORTH, Diretion.SOUTH, Diretion.EAST, Diretion.WEST]



class Board:
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        self.rolling: Set[Point] = set()
        self.static: Set[Point] = set()
        self.prev_cycles: List[Set[Point]] = list()
        self.cycle_index = None

    def add_rolling(self, point: Point):
        if point in self.rolling or point in self.static:
            raise "Cant share spaces"

        self.rolling.add(point)
    
    def add_static(self, point: Point):
        if point in self.rolling or point in self.static:
            raise "Cant share spaces"
        
        self.static.add(point)

    def score(self):
        score = 0
        for point in self.rolling:
            score += (self.height - point.y)
        return score

    def _singular_roll(self, moveables: List[int], statics: List[int], cap:int,  orientation:int):
        class Slot:
            def __init__(self, start, end, orientation):
                self.start = start
                self.end = end
                self.val = self.start if orientation < 0 else self.end
                self.orientation = orientation
                self.range = range(start, end)
                self.items = set()
            
            def __contains__(self, item):
                return item in self.range
            
            def add(self):
                self.val = self.val - orientation
                self.items.add(self.val)

        s = sorted(statics + [-1, cap])
        start = None
        slots = []
        for end in s:
            if start is not None:
                slots.append(Slot(start, end, orientation))
            start = end

        
        for m in moveables:
            for slot in slots:
                if m in slot:
                    slot.add()
                    break
        
        result = []
        for slot in slots:
            for item in slot.items:
                result.append(item)
        
        return result
    
    def multi_cycle(self, count):
        cycle_start = None
        cycle_end = None
        prev_cycles = []

        for i in range(count):
            prev_cycles.append(self.rolling)
            self.cycle()

            if self.rolling in prev_cycles:
                cycle_end = i
                cycle_start = prev_cycles.index(self.rolling)
                break
        
        idx = ((count - cycle_start) % (cycle_end - cycle_start + 1)) + cycle_start

        self.rolling = prev_cycles[idx]



    def cycle(self):
        self.roll(Diretion.NORTH)
        self.roll(Diretion.WEST)
        self.roll(Diretion.SOUTH)
        self.roll(Diretion.EAST)
    
    def roll(self, direction: Point):
        if not Diretion.valid(direction):
            raise "Direction Not Valid"
        
        new_rolling: Set[Point] = set()

        axis = 0 if direction[0] == 0 else 1
        anti_axis = 0 if axis else 1
        orientation = direction[anti_axis]
        cap = self.width if axis else self.height

        for slot in range(cap):
            rolling = [p[anti_axis] for p in self.rolling if p[axis] == slot]
            static = [p[anti_axis] for p in self.static if p[axis] == slot]
            rolled = self._singular_roll(rolling, static, cap, orientation)
            for new in rolled:
                t = [slot, slot]
                t[anti_axis] = new
                new_rolling.add(Point(*t))

        self.rolling = new_rolling

    def print(self):
        for y in range(self.height):
            s = '> '
            for x in range(self.width):
                c = ColoredString('.', TerminalColor.BLACK)
                if (y,x) in self.static:
                    c = ColoredString('#', TerminalColor.GREEN)
                if (y,x) in self.rolling:
                    c = ColoredString('O', TerminalColor.CYAN)
                s += str(c)
            print(s)
                    

class DayFourteen(Solution):
    command_name='d14'

    def part_one(self):
        lines = self.input_data.splitlines()
        width = len(lines[0])
        height = len(lines)

        board = Board(height, width)
        
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == 'O':
                    board.add_rolling(Point(y,x))
                if c == '#':
                    board.add_static(Point(y,x))

        board.roll(Diretion.NORTH)
        
        return board.score()
    
    def part_two(self):
        lines = self.input_data.splitlines()
        width = len(lines[0])
        height = len(lines)

        board = Board(height, width)
        
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == 'O':
                    board.add_rolling(Point(y,x))
                if c == '#':
                    board.add_static(Point(y,x))
                    
        board.multi_cycle(1_000_000_000)
        return board.score()

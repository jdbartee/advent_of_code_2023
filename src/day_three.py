from .aoc_lib import Solution, ColoredString, TerminalColor
from dataclasses import dataclass, field
from typing import List


@dataclass
class Point:
    x: int
    y: int

class PartNumber:
    def __init__(self) -> None:
        self.start: Point = None
        self.end: Point = None
        self.value: int = None

    def is_adjecent_to(self, point: Point) -> bool:
        if point.y < self.start.y - 1 or point.y > self.start.y + 1:
            return False
        start = self.start.x - 1
        end = self.end.x + 1

        if point.x < start or point.x > end:
            return False
        
        return True

@dataclass
class Schematic:
    parts: List[PartNumber] = field(default_factory=list)
    symbols: List[Point] = field(default_factory=list)
    size: Point = field(default_factory=lambda: Point(0,0))
    gears: List[Point] = field(default_factory=list)

    @classmethod
    def load(cls, text: str) -> 'Schematic':
        schematic = Schematic()

        for (y, line) in enumerate(text.splitlines()):
            acc_start = Point(0,0)
            acc = None
            line = line + '.'
            for (x, c) in enumerate(line):
                if c.isdigit():
                    if acc is None:
                        acc_start = Point(x, y)
                        acc = c
                    else:
                        acc = acc + c
                else:
                    if acc is not None:
                        part = PartNumber()
                        part.start = acc_start
                        part.end = Point(x-1, y)
                        part.value = int(acc)
                        schematic.parts.append(part)
                        acc = None

                    if c == '*':
                        schematic.gears.append(Point(x,y))
                
                    if c != '.':
                        schematic.symbols.append(Point(x, y))
        schematic.size = Point(x, y)
        return schematic

    def debug_print(self):
        chars = [[ColoredString('.') for _ in range(self.size.x)] for _ in range(self.size.y + 1)]
        for symbol in self.symbols:
            chars[symbol.y][symbol.x] = ColoredString(char='X', color=TerminalColor.MAGENTA)

        for symbol in self.gears:
            chars[symbol.y][symbol.x].char = '*'
            count = 0
            for part in self.parts:
                if part.is_adjecent_to(symbol):
                    count += 1
            if count == 2:
                chars[symbol.y][symbol.x].color = TerminalColor.CYAN
        for part in self.parts:
            color = TerminalColor.RED
            for symbol in self.symbols:
                if part.is_adjecent_to(symbol):
                    color = TerminalColor.GREEN
            s = str(part.value)
            for (o,c) in enumerate(s):
                chars[part.start.y][part.start.x + o] = ColoredString(c, color)
    
        for line in chars:
            for char in line:
                print(char, end='')
            print('')

class DayThree(Solution):
    command_name = 'd3'

    def part_one(self):
        schem = Schematic.load(self.input_data)
        acc = 0
        for part in schem.parts:
            for symbol in schem.symbols:
                if part.is_adjecent_to(symbol):
                    acc += part.value
                    break

        return acc
    
    def part_two(self):
        schem = Schematic.load(self.input_data)
        acc = 0

        for gear in schem.gears:
            parts = []
            for part in schem.parts:
                if part.is_adjecent_to(gear): parts.append(part)
            if len(parts) == 2:
                acc += parts[0].value * parts[1].value
        
        return acc

from dataclasses import dataclass
from typing import Set, Tuple
from .aoc_lib import Solution


@dataclass
class DigCommand:
    dx: int
    dy: int
    line: str

    @classmethod
    def from_line(cls, line: str):
        d, m, c = line.split(' ')
        dx = 0
        dy = 0
        if d == 'R':
            dx = int(m)
        elif d == 'L':
            dx = -int(m)
        elif d == 'U':
            dy = -int(m)
        elif d == 'D':
            dy = int(m)
        return cls(dx, dy, line)
    
    @classmethod
    def from_line_color(cls, line: str):
        _, _, c = line.split(' ')
        c = c.strip('(#)')
        m = int(c[:5], 16)
        d = c[5]
        dx = 0
        dy = 0
        if d == '0':
            dx = int(m)
        elif d == '2':
            dx = -int(m)
        elif d == '3':
            dy = -int(m)
        elif d == '1':
            dy = int(m)
        return cls(dx, dy, line)


def det(y1, x1, y2, x2):
    return x1 * y2 - x2 * y1

def sign(a):
    if a > 0:
        return 1
    if a < 0:
        return -1
    return 0

class ShoelaceDigMap:
    def __init__(self) -> None:
        self.left_hand_points = []
        self.right_hand_points = []
        self.current_point = (0,0)
        self.prev_left_vector = None

    def execute(self, command: DigCommand):
        dx = command.dx
        dy = command.dy

        y, x = self.current_point
        new_point = y+dy, x+dx

        mul = 0.5
        sdx = sign(dx)
        sdy = sign(dy)
        left_vector = (-sdx, -sdy)

        if self.prev_left_vector:
            left_point = (
                y - (left_vector[0] * mul) - (self.prev_left_vector[0] * mul),
                x + (left_vector[1] * mul) + (self.prev_left_vector[1] * mul)
            )
            right_point = (
                y + (left_vector[0] * mul) + (self.prev_left_vector[0] * mul),
                x - (left_vector[1] * mul) - (self.prev_left_vector[1] * mul)
            )

            self.left_hand_points.append(left_point)
            self.right_hand_points.append(right_point)

        self.prev_left_vector = left_vector
        self.current_point = new_point
        self.previous_direction = (dy, dx)
    
    def shoelace_area(self, points):
        point_it = iter(points)
        area = 0
        prev = next(point_it)
        for point in point_it:
            area += det(*prev, *point)
            prev = point
        area += det(*prev, *points[0])
        return area / 2

    def get_area(self):
        left = self.shoelace_area(self.left_hand_points)
        right = self.shoelace_area(self.right_hand_points)
        return int(max(left, right))

class DayEighteen(Solution):
    command_name = 'd18'

    def part_one(self):
        commands = [DigCommand.from_line(line) for line in self.input_data.splitlines() if line]
        dig_map = ShoelaceDigMap()
        for command in commands:
            dig_map.execute(command)
        dig_map.execute(commands[0])
        return dig_map.get_area()
    
    def part_two(self):
        commands = [DigCommand.from_line_color(line) for line in self.input_data.splitlines() if line]
        dig_map = ShoelaceDigMap()
        for command in commands:
            dig_map.execute(command)
        dig_map.execute(commands[0])
        return dig_map.get_area()
from typing import List
from .aoc_lib import Solution
from dataclasses import dataclass, field


@dataclass
class Draw:
    red: int = 0
    green: int = 0
    blue: int = 0

    def superset(self, other: 'Draw') -> 'Draw':
        res = Draw()
        res.red = max(self.red, other.red)
        res.blue = max(self.blue, other.blue)
        res.green = max(self.green, other.green)
        return res


@dataclass
class Game:
    id: int
    draws: List[Draw] = field(default_factory=list)

    @classmethod
    def parse(cls, line: str):
        name, draws = line.split(':', 1)
        id_str = name.removeprefix('Game ')
        id_int = int(id_str)
        game = Game(id_int)
        for draw_str in draws.split(';'):
            draw = Draw()
            for count_color in draw_str.split(','):
                count, color = count_color.strip().split(' ', maxsplit=1)
                if color == "red":
                    draw.red = int(count)
                elif color == "green": 
                    draw.green = int(count)
                elif color == "blue":
                    draw.blue = int(count)
                else:
                    print("ERROR!!!")
                    print(f"'{color}'")
                    print(draw_str)
            game.draws.append(draw)
        return game

    def possible_with(self, red: int, green: int, blue: int) -> bool:
        for draw in self.draws:
            if draw.red > red:
                return False
            if draw.green > green:
                return False
            if draw.blue > blue:
                return False
        return True
    
    def power(self) -> int:
        superset = Draw()
        for draw in self.draws:
            superset = superset.superset(draw)
        return superset.red * superset.blue * superset.green


class DayTwo(Solution):
    command_name = 'd2'

    def part_one(self):
        result = 0
        for line in self.input_data.splitlines():
            game = Game.parse(line)
            if game.possible_with(red=12, green=13, blue=14):
                result += game.id
            
        return result

    def part_two(self):
        result = 0
        for line in self.input_data.splitlines():
            game = Game.parse(line)
            result += game.power()
            
        return result
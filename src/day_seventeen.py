from dataclasses import dataclass
from functools import lru_cache
from typing import List
from .aoc_lib import Solution

UP = (-1, 0)
DOWN = (1, 0)
LEFT  = (0, -1)
RIGHT = (0, 1)

def add(a: tuple, b: tuple):
    return (a[0]+b[0], a[1]+b[1])

def mul(a: tuple, b: int):
    return (a[0] * b, a[1] * b)

@dataclass
class Step:
    point: tuple
    direction: tuple
    cost: int

    def visited_hash(self):
        dy = 1 if self.direction[0] else 0
        dx = 1 if self.direction[1] else 0
        py = self.point[0]
        px = self.point[1]

        return (py, px, dy, dx)

class Path:
    def __init__(self) -> None:
        self.cost = 0
        self.steps: List[Step] = []

    def extended(self, step):
        new_path = Path()
        new_path.cost = step.cost + self.cost
        new_path.steps = [step for step in self.steps]
        new_path.steps.append(step)
        return new_path

class Router:
    def __init__(self, map: 'Map', start: tuple, end: tuple) -> None:
        self.map = map
        self.start= start
        self.end = end

    def extend_path(self, path: Path) -> List[Path]:
        res_paths = []
        last_step = path.steps[-1]
        last_point = last_step.point

        directions = []

        if last_step.direction[0] == 0:
            directions.extend([UP, DOWN])

        if last_step.direction[1] == 0:
            directions.extend([LEFT, RIGHT])

        for d in directions:
            total_direction = (0,0)
            total_cost = 0
            for _ in range(3):
                total_direction = add(total_direction, d)
                point = add(last_point, total_direction)
                step_cost = self.map.cost_at(*point)
                if step_cost is None:
                    break
                total_cost += step_cost
                new_step = Step(point, total_direction, total_cost)
                new_path = path.extended(new_step)
                res_paths.append(new_path)

        return res_paths

    
    def route(self) -> 'Path':
        visited = set()

        starting_step = Step(self.start, (0,0), 0)
        starting_path = Path()
        starting_path.steps = [starting_step]
        starting_path.cost = 0

        paths = [starting_path]
        for _ in range(1_000_000):
            path = paths.pop(0)

            if path.steps[-1].visited_hash() in visited:
                continue
            
            visited.add(path.steps[-1].visited_hash())

            if path.steps[-1].point == self.end:
                return path
            
            for new_path in self.extend_path(path):
                paths.append(new_path)

            paths = sorted(paths, key=lambda p: p.cost)
            

class UltraRouter(Router):
    def extend_path(self, path: Path) -> List[Path]:
        res_paths = []
        last_step = path.steps[-1]
        last_point = last_step.point

        directions = []

        if last_step.direction[0] == 0:
            directions.extend([UP, DOWN])

        if last_step.direction[1] == 0:
            directions.extend([LEFT, RIGHT])

        for d in directions:
            total_direction = (0,0)
            total_cost = 0
            for i in range(10):
                total_direction = add(total_direction, d)
                point = add(last_point, total_direction)
                step_cost = self.map.cost_at(*point)
                if step_cost is None:
                    break
                total_cost += step_cost
                if i < 3:
                    continue
                new_step = Step(point, total_direction, total_cost)
                new_path = path.extended(new_step)
                res_paths.append(new_path)

        return res_paths


class Map:
    def __init__(self) -> None:
        self.cost_map = {}
        self.width = {}
        self.height = {}
    
    def cost_at(self, y: int, x: int) -> int:
        return self.cost_map.get((y, x))
    
    @staticmethod
    def load_map(lines):
        m = Map()
        m.height = len(lines)
        m.width = len(lines[0])
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                m.cost_map[(y, x)] = int(c)
        return m


class DaySeventeen(Solution):
    command_name = 'd17'

    def part_one(self):
        cost_map = Map.load_map(self.input_data.splitlines())
        router = Router(cost_map, (0,0), (cost_map.height-1, cost_map.width-1))
        path = router.route()
        return path.cost
    
    def part_two(self):
        cost_map = Map.load_map(self.input_data.splitlines())
        router = UltraRouter(cost_map, (0,0), (cost_map.height-1, cost_map.width-1))
        path = router.route()
        return path.cost
from typing import List, Set
from .aoc_lib import Solution
from dataclasses import dataclass, field

@dataclass
class Galaxy:
    id: int
    x: int
    y: int

    def distance_to(self, other: 'Galaxy') -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

@dataclass
class GalaxyMap:
    xset: Set[int] = field(default_factory=set)
    yset: Set[int] = field(default_factory=set)
    galaxies: List[Galaxy] = field(default_factory=list)

    def add_galaxy(self, galaxy: Galaxy):
        self.xset.add(galaxy.x)
        self.yset.add(galaxy.y)
        self.galaxies.append(galaxy)

    def expand(self, n=1):
        for y in reversed(range(max(self.yset) + 1)):
            if y not in self.yset:
                for galaxy in self.galaxies:
                    if galaxy.y > y:
                        galaxy.y += n

        for x in reversed(range(max(self.xset) + 1)):
            if x not in self.xset:
                for galaxy in self.galaxies:
                    if galaxy.x > x:
                        galaxy.x += n

        self.xset = set()
        self.yset = set()
        for galaxy in self.galaxies:
            self.xset.add(galaxy.x)
            self.yset.add(galaxy.y)


    def print_galaxy_map(self):
        lines = []
        for y in range(max(self.yset)+1):
            line = ""
            for x in range(max(self.xset)+1):
                is_galaxy = False
                for galaxy in self.galaxies:
                    if galaxy.x == x and galaxy.y == y:
                        is_galaxy = galaxy.id
                        break
                line = line + ("#" if is_galaxy else ".")
            lines.append(line)
        for line in lines: print(line)

    def caluculate_distances(self) -> int:
        total = 0
        for galaxy in self.galaxies:
            for other in self.galaxies:
                if other.id > galaxy.id:
                    total += galaxy.distance_to(other)
        return total


class DayEleven(Solution):
    command_name = 'd11'

    def part_one(self):
        ident = 0
        map = GalaxyMap()
        for y, line in enumerate(self.input_data.splitlines()):
            for x, c in enumerate(line):
                if c == "#":
                    ident += 1
                    g = Galaxy(ident, x, y)
                    map.add_galaxy(g)
        map.expand()
        return map.caluculate_distances()
    
    def part_two(self):
        ident = 0
        map = GalaxyMap()
        for y, line in enumerate(self.input_data.splitlines()):
            for x, c in enumerate(line):
                if c == "#":
                    ident += 1
                    g = Galaxy(ident, x, y)
                    map.add_galaxy(g)
        map.expand(n=999_999)
        return map.caluculate_distances()
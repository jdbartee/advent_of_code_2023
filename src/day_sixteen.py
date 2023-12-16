from collections import namedtuple
from dataclasses import dataclass
from typing import Any, Dict, List, Set
from .aoc_lib import Solution


@dataclass
class Vector:
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    def __add__(self, other) -> 'Vector':
        return Vector(self.x + other.x, self.y + other.y)

@dataclass
class Beam:
    position: Vector
    velocity: Vector


class Component:
    def __init__(self) -> None:
        self.previous_vels: Set[Vector] = set()
    
    def move_beam(self, beam: Beam) -> List[Beam]:
        if beam.velocity in self.previous_vels:
            return []
        else:
            self.previous_vels.add(beam.velocity)
            return self.do_movement(beam)
    
    def do_movement(self, beam) -> List[Beam]:
        return [beam]
    
class Floor(Component):
    def do_movement(self, beam: Beam) -> List[Beam]:
        new_pos = beam.position + beam.velocity
        return [Beam(new_pos, beam.velocity)]


class PMirror(Floor):
    """/"""
    def do_movement(self, beam: Beam) -> List[Beam]:
        return super().do_movement(Beam(beam.position, Vector(-beam.velocity.y, -beam.velocity.x)))
    
class NMirror(Floor):
    """\\"""
    def do_movement(self, beam: Beam) -> List[Beam]:
        return super().do_movement(Beam(beam.position, Vector(beam.velocity.y, beam.velocity.x)))

class VSplitter(Floor):
    def do_movement(self, beam: Beam) -> List[Beam]:
        if beam.velocity.x:
            return [
                Beam(beam.position, Vector(0, 1)),
                Beam(beam.position, Vector(0, -1))
            ]
        else:
            return super().do_movement(beam)

class HSplitter(Floor):
    def do_movement(self, beam: Beam) -> List[Beam]:
        if beam.velocity.y:
            return [
                Beam(beam.position, Vector(1, 0)),
                Beam(beam.position, Vector(-1, 0))
            ]
        else:
            return super().do_movement(beam)


class Arena:
    def __init__(self):
        self.components: Dict[Vector, Component] = {}
        self.energized: Set[Vector] = set() 
        self.beams: List[Beam] = []
        self.width = 0
        self.height = 0

    def add_component(self, x, y, component):
        self.width = max(self.width, x+1)
        self.height = max(self.height, y+1)
        self.components[Vector(x, y)] = component

    def tick(self):
        new_beams = []
        for beam in self.beams:
            if beam.position in self.components:
                self.energized.add(beam.position)
                new_beams.extend(self.components[beam.position].move_beam(beam))
        self.beams = new_beams

    def reset(self):
        self.beams = []
        self.energized.clear()
        for com in self.components.values():
            com.previous_vels.clear()

    def count_energy(self, beam: Beam):
        try:
            self.reset()
            self.beams = [beam]
            while self.beams:
                self.tick()
            return len(self.energized)
        finally:
            self.reset()

class DaySixteen(Solution):
    command_name = 'd16'

    def load_arena(self) -> Arena:
        arena = Arena()
        for y, line in enumerate(self.input_data.splitlines()):
            for x, c in enumerate(line):
                if c == '.':
                    arena.add_component(x, y, Floor())
                if c == '|':
                    arena.add_component(x, y, VSplitter())
                if c == '-':
                    arena.add_component(x, y, HSplitter())
                if c == '/':
                    arena.add_component(x, y, PMirror())
                if c == '\\':
                    arena.add_component(x, y, NMirror())
        return arena

    def part_one(self):
        
        beam = Beam(Vector(0, 0), Vector(1, 0))
        arena = self.load_arena()
        return arena.count_energy(beam)
    
    def part_two(self):
        arena = self.load_arena()
        maximum = 0
        for y in range(arena.height):
            lbeam = Beam(Vector(0, y), Vector(1, 0))
            rbeam = Beam(Vector(arena.width-1, y), Vector(-1, 0))
            maximum = max(maximum, arena.count_energy(lbeam))
            maximum = max(maximum, arena.count_energy(rbeam))
        
        for x in range(arena.width):
            tbeam = Beam(Vector(x, 0), Vector(0, 1))
            bbeam = Beam(Vector(x, arena.height-1), Vector(0, -1))
            maximum = max(maximum, arena.count_energy(tbeam))
            maximum = max(maximum, arena.count_energy(bbeam))

        return maximum

from dataclasses import dataclass
from typing import List
from .aoc_lib import Solution


class Command(str):

    def aciton(self):
        if '=' in self:
            label, focal_length = self.split('=')
            lens = Lens(label, int(focal_length))
            return ('add', christmas_hash(label), lens)
        else:
            label = self[:-1]
            return ('remove', christmas_hash(label), label)

@dataclass
class Lens():
    label: str
    focal_length: int
    

class Box:
    def __init__(self) -> None:
        self.lenses: List[Lens] = []

    def add_lens(self, lens: Lens):
        for i, l in enumerate(self.lenses):
            if l.label == lens.label:
                self.lenses[i] = lens
                return
        else:
            self.lenses.append(lens)

    def remove_lens(self, label: str):
        for i, l in enumerate(self.lenses):
            if l.label == label:
                del self.lenses[i]
                return
            
class BoxArray:
    def __init__(self) -> None:
        self.array: List[Box] = [Box() for _ in range(256)]

    def run_command(self, command: Command):
        action, idx, val = command.aciton()
        if action == 'add':
            self.array[idx].add_lens(val)
        else:
            self.array[idx].remove_lens(val)

    def score(self):
        total = 0
        for box_score, box in enumerate(self.array, 1):
            for slot_score, lens in enumerate(box.lenses, 1):
                total += (box_score * slot_score * lens.focal_length)
        return total

    def print(self):
        for i, box in enumerate(self.array):
            if len(box.lenses):
                print(f"Box {i}")
                print(box.lenses)

def christmas_hash(s: str):
    h = 0
    for c in s:
        h = ((h + ord(c)) * 17) % 256
    return h

class DayFifteen(Solution):
    command_name = 'd15'

    def part_one(self):
        parts = self.input_data.split(',')
        hashes = [christmas_hash(p) for p in parts]
        return sum(hashes)
    
    def part_two(self):
        commands = [Command(s) for s in self.input_data.split(',')]
        boxes = BoxArray()
        for command in commands:
            boxes.run_command(command)
        
        return boxes.score()

        
        
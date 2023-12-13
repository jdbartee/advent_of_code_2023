from dataclasses import dataclass
from functools import lru_cache
from typing import List

from .aoc_lib import Solution

OFF="#"
ON="."
UNKNOWN="?"

@dataclass
class InputRow:
    fields: str
    clues: List[int]

    def __hash__(self) -> int:
        return hash((self.fields, *self.clues))

    @classmethod
    def parse(cls, line: str):
        fields, clues_str = line.split(' ')
        clues = [int(clue) for clue in clues_str.split(',')]
        return cls(fields, clues)
    
    @lru_cache
    def get_possibilities(self, field_idx: int = 0, clue_index: int = 0):
        fields = self.fields[field_idx:]
        clues = self.clues[clue_index:]
        
        if not fields:
            if not clues:
                return 1
            else:
                return 0
            
        if not clues:
            if OFF not in fields:
                return 1
            else:
                return 0
        
        clue = clues[0]
        if len(fields[:clue]) != clue: return 0
        
        count = 0

        if ON not in fields[:clue] and OFF not in fields[clue:clue+1]:
            count += self.get_possibilities(field_idx + clue + 1, clue_index+1)
        if OFF not in fields[:1]:
            count += self.get_possibilities(field_idx + 1, clue_index)

        return count
    
    def unfold(self):
        fields = UNKNOWN.join([self.fields] * 5)
        clues = self.clues * 5
        return InputRow(fields, clues)


class DayTwelve(Solution):
    command_name = 'd12'

    def part_one(self):
        total = 0
        for line in self.input_data.splitlines():
            input_row = InputRow.parse(line)
            total += input_row.get_possibilities()
        return total
    
    def part_two(self):
        total = 0
        for line in self.input_data.splitlines():

            input_row = InputRow.parse(line).unfold()
            total += input_row.get_possibilities()
        return total
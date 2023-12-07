from typing import List, Tuple
from .aoc_lib import Solution
from dataclasses import dataclass
from itertools import chain

@dataclass
class Mapping:
    source_start: int
    dest_start: int
    length: int

    def applicable(self, val: int) -> bool:
        return val in range(self.source_start, self.source_start + self.length)
    
    def i_applicable(self, val: int) -> bool:
        return val in range(self.dest_start, self.dest_start + self.length)
    
    def apply(self, val: int) -> int:
        return val - self.source_start + self.dest_start
    
    def i_apply(self, val: int) -> int:
        return val - self.dest_start + self.source_start
    
    def map_range(self, r: range) -> Tuple[range, range, range]:
        if r.stop < self.source_start:
            return (None, r, None)
        
        if r.start > self.source_start + self.length:
            return (None, None, r)
        
        start = self.source_start
        end = self.source_start + self.length

        prefix_start = r.start if r.start < start else None
        prefix_end = start

        overlap_start = r.start if self.applicable(r.start) else start
        overlap_end = r.stop if self.applicable(r.stop) else end

        postfix_start = end if end < r.stop else None
        postfix_end = r.stop

        return (range(self.apply(overlap_start), self.apply(overlap_end)), 
                range(prefix_start, prefix_end) if prefix_start else None, 
                range(postfix_start, postfix_end) if postfix_start else None)

    
            

    
    @classmethod
    def parse(cls, line: str):
        parts = line.split(' ')
        return cls(source_start=int(parts[1]),
                   dest_start=int(parts[0]),
                   length=int(parts[2]))

class Mapper:
    def __init__(self) -> None:
        self.mappings: List[Mapping] = []

    def add_mapping(self, mapping: Mapping):
        self.mappings.append(mapping)
        
    def map(self, val: int) -> int:
        for mapping in self.mappings:
            if mapping.applicable(val):
                return mapping.apply(val)
        
        return val
    
    def i_map(self, val: int) -> int:
        for mapping in self.mappings:
            if mapping.i_applicable(val):
                return mapping.i_apply(val)
        
        return val
    
    def map_ranges(self, to_map: List[range]) -> List[range]:
        mapped = []
        for mapping in self.mappings:
            next_iter = []
            for x in to_map:
                m, pre, post = mapping.map_range(x)
                if pre: next_iter.append(pre)
                if post: next_iter.append(post)
                if m: mapped.append(m)
            to_map = next_iter
        mapped.extend(next_iter)
        return mapped

    

def is_in_any_range(val: int, ranges) -> bool:
    return any(val in r for r in ranges)

class DayFive(Solution):
    command_name = 'd5'

    def part_one(self):
        seeds = []
        mappers = [Mapper() for _ in range(7)]
        line_it =  iter(self.input_data.splitlines())
        line = next(line_it)
        _, seeds_str = line.split(':')
        seeds = [int(seed) for seed in seeds_str.split(' ') if seed]
        mapper_idx = -1
        for line in line_it:
            if line.endswith(':'):
                mapper_idx +=1
                continue
            if line:
                mappers[mapper_idx].add_mapping(Mapping.parse(line))

        for mapper in mappers:
            for i, seed in enumerate(seeds):
                seeds[i] = mapper.map(seed)

        return min(seeds)

    def part_two(self):
        seeds = []
        mappers = [Mapper() for _ in range(7)]
        line_it =  iter(self.input_data.splitlines())
        line = next(line_it)
        _, seeds_str = line.split(':')
        seeds_it = iter([int(seed) for seed in seeds_str.split(' ') if seed])
        seeds = []
        while True:
            try:
                start = next(seeds_it)
                length = next(seeds_it)
            except StopIteration:
                break
            seeds.append(range(start, start+length))

        
        mapper_idx = -1
        for line in line_it:
            if line.endswith(':'):
                mapper_idx +=1
                continue
            if line:
                mappers[mapper_idx].add_mapping(Mapping.parse(line))

        for mapper in mappers:
            seeds = mapper.map_ranges(seeds)

        return min(r.start for r in seeds)
        
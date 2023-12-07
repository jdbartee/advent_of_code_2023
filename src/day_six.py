from .aoc_lib import Solution
from dataclasses import dataclass
from math import sqrt, floor, ceil

epsilon = 0.00000001

@dataclass
class Race:
    time: int
    record: int

    def optimum(self) -> float:
        return 0.5 * self.time
    
    def run(self, button_time: int) -> int:
        return self.time*button_time - button_time**2

    def inverse(self, distance) -> float:
        return 0.5 * (self.time + sqrt(self.time**2 -4 * distance))

    def margin_of_error(self) -> int:
        optimum = self.optimum()
        record = self.inverse(self.record)

        dist = abs(optimum - record) - epsilon
        min = ceil(optimum - dist)
        max = floor(optimum + dist)

        return len(range(min, max+1))
    


class DaySix(Solution):
    command_name = 'd6'

    def load_races(self):
        lines = self.input_data.splitlines()
        times = []
        distances = []
        races = []

        for line in lines:
            if line.startswith('Time'):
                _, time_strs = line.split(':', maxsplit=1)
                times = [int(time) for time in time_strs.split(' ') if time]
            if line.startswith('Distance'):
                _, dist_strs = line.split(':', maxsplit=1)
                distances = [int(dist) for dist in dist_strs.split(' ') if dist]
        
        if len(times) != len(distances):
            breakpoint()
            raise "Races don't match"
        
        for i, time in enumerate(times):
            races.append(Race(time=time, record=distances[i]))

        return races
    
    def load_single_race(self):
        lines = self.input_data.splitlines()
        time = 0
        distance = 0

        for line in lines:
            if line.startswith('Time'):
                _, time_strs = line.split(':', maxsplit=1)
                time = int(time_strs.replace(' ', ''))
            if line.startswith('Distance'):
                _, dist_strs = line.split(':', maxsplit=1)
                distance = int(dist_strs.replace(' ', ''))

        return Race(time, distance)

            

    def part_one(self):
        races = self.load_races()
        res = 1
        for race in races:
            res *= race.margin_of_error()
        return res
    
    def part_two(self):
        race = self.load_single_race()
        return race.margin_of_error()
    
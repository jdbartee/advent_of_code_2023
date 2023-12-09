from .aoc_lib import Solution
from math import lcm

class Network:
    def __init__(self):
        self.map = {}
    
    def add_line(self, line: str):
        parts = [part.strip() for part in line.split('=')]
        source = parts[0]
        targets = [part.strip() for part in parts[1].lstrip('(').rstrip(')').split(',')]
        self.map[source] = targets

    def navigate(self, diretions: str):
        current = 'AAA'
        count = 0
        while True:
            for c in diretions:
                if current == 'ZZZ':
                    return count
                count += 1
                current = self.map[current][0 if c == 'L' else 1]

    def ghost_navigate(self, directions: str):
        starts = [key for key in self.map.keys() if key.endswith('A')]
        
        info = {
            start: {
                'loop_start': None,
                'loop_start_c': None,
                'loop_len': None,
                'pre_loop_zees': [],
                'post_loop_zees': []
            } 
            for start in starts
        }

        for start in starts:
            count = 0
            begins = set()
            current = start
            while current not in begins:
                begins.add(current)
                for c in directions:
                    count += 1
                    current = self.map[current][0 if c == 'L' else 1]
                    if current.endswith('Z'):
                        info[start]['pre_loop_zees'].append(count)
            info[start]['loop_start'] = current
            info[start]['loop_start_c'] = count

            loop_point = current
            count = 0
            go = True
            while go:
                for c in directions:
                    count += 1
                    current = self.map[current][0 if c == 'L' else 1]
                    if current.endswith('Z'):
                        info[start]['post_loop_zees'].append(count)
                if current == loop_point:
                    go = False
                    info[start]['loop_len'] = count

        ret = 1
        for item in info.values():
            ret = lcm(ret, item['loop_len'])

        return ret
            
        


class DayEight(Solution):
    command_name = 'd8'

    def part_one(self):
        return None
        line_it = iter(self.input_data.splitlines())
        directions = next(line_it)
        skip = next(line_it)
        network = Network()
        for line in line_it:
            network.add_line(line)
        return network.navigate(directions)
    
    def part_two(self):
        line_it = iter(self.input_data.splitlines())
        directions = next(line_it)
        skip = next(line_it)
        network = Network()
        for line in line_it:
            network.add_line(line)
        return network.ghost_navigate(directions)


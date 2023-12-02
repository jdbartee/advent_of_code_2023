from .aoc_lib import Solution


class DayOne(Solution):
    command_name = 'd1'

    def part_one(self):
        values = []
        for line in self.input_data.splitlines():
            first = None
            last = None
            for c in line:
                if c.isdigit():
                    if first is None:
                        first = int(c) * 10
                    last = int(c)
            try:
                values.append(first + last)
            except: pass
        return sum(values)

    def part_two(self):
        values = []
        for line in self.input_data.splitlines():
            line = line.replace('one', 'one1one')
            line = line.replace('two', 'two2two')
            line = line.replace('three', 'three3three')
            line = line.replace('four', 'four4four')
            line = line.replace('five', 'five5five')
            line = line.replace('six', 'six6six')
            line = line.replace('seven', 'seven7seven')
            line = line.replace('eight', 'eight8eight')
            line = line.replace('nine', 'nine9nine')
            first = None
            last = None
            for c in line:
                if c.isdigit():
                    if first is None:
                        first = int(c) * 10
                    last = int(c)
            try:
                values.append(first + last)
            except:
                breakpoint()
        return sum(values)

            

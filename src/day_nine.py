from .aoc_lib import Solution


def extrapolate_forward(seq):
    reduced = reduce(seq)
    if all(i == 0 for i in reduced):
        diff = 0
    else:
        diff = extrapolate_forward(reduced)
    return seq[-1] + diff

def extrapolate_backward(seq):
    reduced = reduce(seq)
    if all(i == 0 for i in reduced):
        diff = 0
    else:
        diff = extrapolate_backward(reduced)
    
    return seq[0] - diff

def reduce(seq):
    return [seq[i] - seq[i-1] for i in range(1, len(seq))]

def parse_seq(line):
    return [int(i) for i in line.split()]

class DayNine(Solution):
    command_name = 'd9'
    
    def part_one(self):
        seqs = [parse_seq(line) for line in self.input_data.splitlines()]
        preds = [extrapolate_forward(seq) for seq in seqs]
        return sum(preds)
    

    def part_two(self):
        seqs = [parse_seq(line) for line in self.input_data.splitlines()]
        preds = [extrapolate_backward(seq) for seq in seqs]
        return sum(preds)

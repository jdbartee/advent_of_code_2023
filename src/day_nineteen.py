from dataclasses import dataclass
from .aoc_lib import Solution
from copy import deepcopy

@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def total(self):
        return self.x + self.m + self.a + self.s

    @classmethod
    def parse(cls, text: str):
        text = text.strip('{}')
        defs = text.split(',')
        x,m,a,s = 0,0,0,0

        for d in defs:
            name, val = d.split('=')
            if name == 'x': x = int(val)
            if name == 'm': m = int(val)
            if name == 'a': a = int(val)
            if name == 's': s = int(val)

        return cls(x,m,a,s)

class Rule():
    def __init__(self) -> None:
        self.target = None
        self.key = None
        self.op = None
        self.value = None

    def matches(self, part: Part):
        if self.key is None: return True

        if self.op == '<':
            return part.__dict__[self.key] < self.value
        if self.op == '>':
            return part.__dict__[self.key] > self.value
        
    def ranges(self):
        if self.op == '<':
            return (
                range(1, self.value),
                range(self.value, 4001)
            )
        if self.op == '>':
            return (
                range(self.value+1, 4001),
                range(1, self.value+1)
            )

        
    @classmethod
    def parse(cls, text: str):
        rule = cls()
        if ':' not in text:
            rule.target = text
            return rule
        
        cond, target = text.split(':')
        rule.target = target
        rule.key = cond[0]
        rule.op = cond[1]
        rule.value = int(cond[2:])
        return rule

def range_intersect(a: range, b: range):
    start = max(a.start, b.start)
    stop = min(a.stop, b.stop)
    return range(start, stop)

class WorkFlow():
    def __init__(self) -> None:
        self.rules = []

    def process(self, part: Part):
        for rule in self.rules:
            if rule.matches(part):
                return rule.target
        raise "No fallthrough rule"
    
    @classmethod
    def parse(cls, text):
        text = text.strip('{}')
        parts = text.split(',')
        workflow = cls()
        workflow.rules = [Rule.parse(p) for p in parts]
        return workflow


class System():
    def __init__(self):
        self.workflows = {}
        self.accepted_count = 0
        self.accepted_score = 0

    def process(self, part: Part):
        workflow_id = 'in'
        while workflow_id not in ('A', 'R'):
            workflow = self.workflows[workflow_id]
            workflow_id = workflow.process(part)
        if workflow_id == 'A':
            self.accepted_count += 1
            self.accepted_score += part.total()

    def add_workflow(self, text: str):
        name, rules = text.split('{')
        self.workflows[name] = WorkFlow.parse(rules)

    def count_rule(self, ranges, workflow_id, index):
        if workflow_id == 'A':
            return (len(ranges['x']) * 
                    len(ranges['m']) *
                    len(ranges['a']) *
                    len(ranges['s']))

        if workflow_id == 'R':
            return 0
        
        rule: Rule = self.workflows[workflow_id].rules[index]
        if not rule.key:
            return self.count_rule(ranges, rule.target, 0)
        
        left_range, right_range = rule.ranges()
        right_ranges = deepcopy(ranges)

        ranges[rule.key] = range_intersect(ranges[rule.key], left_range)
        right_ranges[rule.key] = range_intersect(right_ranges[rule.key], right_range)

        left_count = self.count_rule(ranges, rule.target, 0)
        right_count = self.count_rule(right_ranges, workflow_id, index+1)

        return left_count + right_count


    def count(self):
        ranges = {
            'x': range(1, 4001),
            'm': range(1, 4001),
            'a': range(1, 4001),
            's': range(1, 4001),
        }
        return self.count_rule(ranges, 'in', 0)

        
class DayNineteen(Solution):
    command_name = 'd19'

    def part_one(self):
        lines = [line.strip() for line in self.input_data.splitlines() if line.strip()]

        system = System()
        parts = []
        for line in lines:
            if line.startswith('{'):
                parts.append(Part.parse(line))
            else:
                system.add_workflow(line)
        
        for part in parts:
            system.process(part)

        return system.accepted_score

    def part_two(self):
        from datetime import datetime
        lines = [line.strip() for line in self.input_data.splitlines() if line.strip()]

        system = System()
        for line in lines:
            if line.startswith('{'):
                pass
            else:
                system.add_workflow(line)
        return system.count()
from dataclasses import dataclass
from typing import Dict, List
from .aoc_lib import Solution
from math import lcm


class Value(int):...

@dataclass
class Signal:
    High = 1
    Low = -1
    value: Value
    source: str

@dataclass
class DirectedSignal:
    target: str
    signal: Signal

    def __str__(self) -> str:
        return f'{self.signal.source} -{"low" if self.signal.value == Signal.Low else "high"}-> {self.target}'

class Dispatcher:
    def __init__(self):
        self.dispatch_queue: List[DirectedSignal] = []
        self.nodes: Dict[str, 'Node'] = {}
        self.connections: Dict[str, List[str]] = {}
        self.low_count = 0
        self.high_count = 0
        self.button_count = 0
        self.machine_activated = False

    def reset(self):
        self.button_count = 0
        self.low_count = 0
        self.high_count = 0
        for node in self.nodes.values():
            node.reset()
    
    def button(self):
        self.button_count += 1
        self.low_count += 1
        self.emit_signal(Signal(Signal.Low, 'broadcaster'))

        while self.dispatch_queue:
            signal = self.dispatch_queue.pop(0)
            if signal.signal.value == Signal.Low:
                self.low_count += 1
            if signal.signal.value == Signal.High:
                self.high_count += 1
            if signal.target in self.nodes:
                node = self.nodes[signal.target]
                node.recieve(signal.signal)
            if signal.target == 'rx' and signal.signal.value == Signal.Low:
                self.machine_activated = True

    def get_dependents(self, name: str):
        dependents = set()
        step_dependents = {name}

        while dependents != step_dependents:
            dependents = {item for item in step_dependents}
            step_dependents = set()
            for item in dependents:
                for source, dest in self.connections.items():
                    if item in dest:
                        step_dependents.add(source)
        if 'broadcaster' in dependents:
            dependents.remove('broadcaster')
        return dependents
    
    def find_loop(self, name: str):
        self.reset()
        dependents = list(self.get_dependents(name))
        states = set()
        states_dict = {}

        for _ in range(100_000):
            state = tuple(self.nodes[k].state_hash() for k in dependents)
            states_dict[(self.button_count, self.low_count, self.high_count)] = state
            if state in states:
                return self.button_count
            states.add(state)
            self.button()

    def part_two(self):
        value = 1
        for node in self.nodes.values():
            if type(node) == FlipFlopNode:
                count = self.find_loop(node.name)
                value = lcm(count, value)
        return value



    def log(self, message):
        signal_count = self.low_count + self.high_count
        print(f"{signal_count}   --   {message}")

    def emit_signal(self, signal):
        for target in self.connections[signal.source]:
            self.dispatch_queue.append(DirectedSignal(target, signal))

    def hookup(self):
        for source, targets in self.connections.items():
            for target in targets:
                if target in self.nodes:
                    target_node = self.nodes[target]
                    target_node.connect(source)
    
    def parse_line(self, line: str):
        source, target = [s.strip() for s in line.split('->')]
        targets = [s.strip() for s in target.split(',')]
        if source == 'broadcaster':
            self.connections[source] = targets
        if source.startswith('%'):
            name = source[1:]
            node = FlipFlopNode(name, self)
            self.nodes[name] = node
            self.connections[name] = targets
        if source.startswith('&'):
            name = source[1:]
            node = ConjunctionNode(name, self)
            self.nodes[name] = node
            self.connections[name] = targets
        
        

class Node:
    def __init__(self, name: str,  dispatcher: Dispatcher):
        self.name = name
        self.dispatcher = dispatcher

    def emit(self, value: Value):
        self.dispatcher.emit_signal(Signal(value, self.name))

    def connect(self, source: str):...
    def recieve(self, signal: Signal):...
    def reset(self):...
    def state_hash(self):
        return ()

    def __str__(self) -> str:
        return self.name

class FlipFlopNode(Node):
    def __init__(self, name: str, dispatcher: Dispatcher):
        super().__init__(name, dispatcher)
        self.on = False

    def __str__(self) -> str:
        return f'{self.name}: {"On" if self.on else "Off"}'
    
    def state_hash(self):
        return (self.on,)
    def reset(self):
        self.on = False
        return super().reset()
    
    def recieve(self, signal: Signal):
        if signal.value == Signal.Low:
            self.on = not self.on
            self.emit(Signal.High if self.on else Signal.Low)
        
        return super().recieve(signal)

class ConjunctionNode(Node):
    def __init__(self, name: str, dispatcher: Dispatcher):
        super().__init__(name, dispatcher)
        self.memory: Dict[str, Value] = {}

    def __str__(self) -> str:
        return f'{self.name}: {self.memory}'
    
    def connect(self, source: str):
        self.memory[source] = Signal.Low
        return super().connect(source)
    
    def state_hash(self):
        values = [self.memory[k] for k in sorted(self.memory.keys())]
        return tuple(values)

    def reset(self):
        for k in self.memory:
            self.memory[k] = Signal.Low
        return super().reset()
    
    def recieve(self, signal: Signal):
        self.memory[signal.source] = signal.value
        if all(v == Signal.High for v in self.memory.values()):
            self.emit(Signal.Low)
        else:
            self.emit(Signal.High)

        return super().recieve(signal)


class DayTwenty(Solution):
    command_name = 'd20'

    def part_one(self):
        dispatcher = Dispatcher()
        for line in self.input_data.splitlines():
            dispatcher.parse_line(line)
        dispatcher.hookup()
        
        for _ in range(1000):
            dispatcher.button()

        return dispatcher.low_count * dispatcher.high_count
    
    def part_two(self):
        dispatcher = Dispatcher()
        for line in self.input_data.splitlines():
            dispatcher.parse_line(line)
        dispatcher.hookup()

        return dispatcher.part_two()


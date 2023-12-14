from typing import List, Set
from .aoc_lib import Solution


class Fold():
    def __init__(self,index=1, vertical=True):
        self.vertical = vertical
        self.index = index

    def score(self):
        if self.vertical: 
            return self.index
        else:
            return 100 * self.index
    
    def matches(self, note: 'Note', threshold=0) -> bool:
        for xa in range(note.width):
            if self.vertical:
                if xa >= self.index: break
                xb = self.index + (self.index - xa) - 1
                if xb > note.width-1: continue
            else:
                xb = xa
            for ya in range(note.height):
                if not self.vertical:
                    if ya >= self.index: break
                    yb = self.index + (self.index - ya) - 1
                    if yb > note.height-1: continue
                else:
                    yb = ya

                if note.lines[ya][xa] != note.lines[yb][xb]:
                    threshold -= 1
                    if threshold < 0:
                        return False
     
        return threshold == 0

class Note:
    def __init__(self) -> None:
        self.lines: List[str] = []

    @property
    def width(self):
        return len(self.lines[0])
    
    @property
    def height(self):
        return len(self.lines)
    
    def score(self, threshold=0):
        folds: Set[Fold] = set()
        for x in range(1, self.width):
            folds.add(Fold(x))
        for x in range(1, self.height):
            folds.add(Fold(x, False))
        
        folds = [f for f in folds if f.matches(self, threshold=threshold)]
        scores = [f.score() for f in folds]
        return sum(scores)

    def print(self):
        for line in self.lines:
            print(line)


class DayThirteen(Solution):
    command_name = 'd13'

    def part_one(self):
        notes: List[Note] = []
        note = None
        for line in self.input_data.splitlines() + ['']:
            if note is None:
                note = Note()
            if line:
                note.lines.append(line)
            else:
                notes.append(note)
                note = None
        if note:
            notes.append(note)

        return sum(note.score(threshold=0) for note in notes)
    
    def part_two(self):
        notes: List[Note] = []
        note = None
        for line in self.input_data.splitlines() + ['']:
            if note is None:
                note = Note()
            if line:
                note.lines.append(line)
            else:
                notes.append(note)
                note = None
        if note:
            notes.append(note)

        return sum(note.score(threshold=1) for note in notes)

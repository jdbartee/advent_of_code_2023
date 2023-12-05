from typing import Set
from .aoc_lib import Solution
from dataclasses import dataclass, field

@dataclass
class Card:
    name: str = ''
    winning: Set[int] = field(default_factory=set)
    numbers: Set[int] = field(default_factory=set)

    @classmethod
    def parse(cls, text: str):
        card = cls()
        card.name, rest = text.split(':')
        winning, numbers = rest.split('|')
        card.winning = {int(num) for num in winning.split(' ') if num}
        card.numbers = {int(num) for num in numbers.split(' ') if num}
        return card
    
    def count_wins(self) -> int:
        return len(self.winning.intersection(self.numbers))
    
    def points(self) -> int:
        wins = self.count_wins()
        if wins:
            return 2**(wins-1)
        return 0



class DayFour(Solution):
    command_name = 'd4'

    def part_one(self):
        score = 0
        for line in self.input_data.splitlines():
            card = Card.parse(line)
            score += card.points()
        return score
    
    def part_two(self):
        # Get all Cards
        cards = [Card.parse(text) for text in self.input_data.splitlines()]
        # Get count of wins
        wins = [card.count_wins() for card in cards]
        # Default to 1 of each card
        card_counts = [1 for _ in cards]

        # Reverse iterate over the indexes
        for idx in reversed(range(0, len(card_counts))):
            win = wins[idx]
            # For each win - increment that cards card count by the subsequent cards card count.
            for idy in range(idx+1, idx+1+win):
                card_counts[idx] += card_counts[idy]

        return sum(card_counts)
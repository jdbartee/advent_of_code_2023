from .aoc_lib import Solution
from dataclasses import dataclass
from functools import lru_cache, cmp_to_key

card_values = {
    'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2
}

hand_type = {
    'Five': 7,
    'Four': 6,
    'Full': 5,
    'Three': 4,
    'TwoPair': 3,
    'OnePair': 2,
    'HighCard': 1
}


@dataclass
class Hand:
    hand: str
    wager: int
    wilds: str=None

    @lru_cache(0)
    def card_values(self):
        return [ 0 if c == self.wilds else card_values[c] for c in self.hand]
    
    @lru_cache(0)
    def hand_type(self):
        wild_count = 0
        h = {}
        for c in self.hand:
            if c == self.wilds:
                wild_count += 1
                continue
            if not c in h: h[c] = 0
            h[c] += 1
        
        counts = sorted(h.values(), reverse=True)

        if wild_count:
            if len(counts): counts[0] += wild_count
            else: counts = [wild_count]

        if counts[0] == 5: return 'Five'
        if counts[0] == 4: return 'Four'
        if counts[0] == 3:
            if counts[1] == 2: return 'Full'
            else: return 'Three'
        if counts[0] == 2:
            if counts[1] == 2: return 'TwoPair'
            else: return 'OnePair'
        return 'HighCard'
    
    def hand_type_score(self):
        return hand_type[self.hand_type()]

    def compare_hands(hand1: 'Hand', hand2: 'Hand'):
        if hand1.hand_type_score() < hand2.hand_type_score():
            return -1
        elif hand1.hand_type_score() > hand2.hand_type_score():
            return 1
        else:
            values1 = hand1.card_values()
            values2 = hand2.card_values()

            for i, v1 in enumerate(values1):
                v2 = values2[i]
                if v1 < v2: return -1
                if v1 > v2: return 1
            else:
                return 0

class DaySeven(Solution):
    command_name = 'd7'

    def part_one(self):
        hands = []
        for line in self.input_data.splitlines():
            h, w = line.split(' ')
            hand = Hand(h, int(w))
            hands.append(hand)
        
        hands = sorted(hands, key=cmp_to_key(Hand.compare_hands))
        total = 0
        for mul, hand in enumerate(hands, 1):
            total += mul * hand.wager

        return total
    

    def part_two(self):
        hands = []
        for line in self.input_data.splitlines():
            h, w = line.split(' ')
            hand = Hand(h, int(w), wilds='J')
            hands.append(hand)
        
        hands = sorted(hands, key=cmp_to_key(Hand.compare_hands))
        total = 0
        for mul, hand in enumerate(hands, 1):
            total += mul * hand.wager

        return total
from collections import Counter
from enum import Enum, IntEnum
from itertools import combinations
from card import Value

class Rank(IntEnum):
    ROYAL_FLUSH = 1
    STRAIGHT_FLUSH = 2
    FOUR_OF_A_KIND = 3
    FULL_HOUSE = 4
    FLUSH = 5
    STRAIGHT = 6
    THREE_OF_A_KIND = 7
    TWO_PAIR = 8
    PAIR = 9
    HIGH_CARD = 10

class HandRanker:

    def __init__(self):
        
        self.switcher = {
            Rank.ROYAL_FLUSH: self.has_royal_flush,
            Rank.STRAIGHT_FLUSH: self.has_straight_flush,
            Rank.FOUR_OF_A_KIND: self.has_four_of_a_kind,
            Rank.FULL_HOUSE: self.has_full_house,
            Rank.FLUSH: self.has_flush,
            Rank.STRAIGHT: self.has_straight,
            Rank.THREE_OF_A_KIND: self.has_three_of_a_kind,
            Rank.TWO_PAIR: self.has_two_pair,
            Rank.PAIR: self.has_pair,
            Rank.HIGH_CARD: self.has_high_card
        }

        self.ROYAL_CARD_VALUE_SET = set([Value.TEN, Value.JACK, Value.QUEEN, Value.KING, Value.ACE])

    def rank_permutations(self, big_hand):
        min_rank = Rank.HIGH_CARD
        min_rank_hands = []
        min_rank_hand = None

        for card_group in combinations(big_hand.cards, 5):
            hand = Hand(card_group)
            rank, hand = self.rank(hand)

            if rank < min_rank:
                min_rank = rank
                min_rank_hands = [ hand ]

            if rank == min_rank:
                min_rank_hands.append(hand)

        if len(min_rank_hands) == 1:
            min_rank_hand = min_rank_hands[0]
        else:
            while len(min_rank_hands) > 1:
                hand1, hand2 = min_rank_hands[0], min_rank_hands[1]
                tiebreak = self.tiebreak(hand1, hand2)

                if tiebreak > 0:
                    min_rank_hands.pop(1)
                elif tiebreak < 0:
                    min_rank_hands.pop(0)
                else:
                    min_rank_hand = min_rank_hands[0]
                    break

        return min_rank, min_rank_hand

    def rank(self, hand):

        if len(hand) > 5:
            return self.rank_permutations(hand)

        card_suits, card_values = hand.get_suits(), hand.get_values()
        the_rank = Rank.HIGH_CARD

        for rank in Rank:
            if self.switcher[rank](card_suits, card_values):
                the_rank = rank
                break

        return the_rank, hand

    def tiebreak(self, hand1, hand2):
        # > 0 means hand1 is bigger
        # < 0 means hand2 is bigger
        # == 0 means they have the same high card

        if len(hand1) > 5 or len(hand2) > 5:
            raise Error("Only size 5 hands can be tiebroken.")

        rank1 = self.rank(hand1)
        rank2 = self.rank(hand2)

        if rank1 != rank2:
            raise Error("These hands should not be in tiebreak")

        card_values1 = [ card.value for card in hand1.cards ]
        card_values2 = [ card.value for card in hand2.cards ]

        card_values1.sort()
        card_values2.sort()

        ret_val = 0

        while len(card_values1) > 0 and len(card_values2) > 0:
            value_1, value_2 = card_values1.pop(), card_values2.pop()

            if value_1 > value_2:
                ret_val = 1
                break

            if value_1 < value_2:
                ret_val = -1
                break

        return ret_val

    def has_royal_flush(self, card_suits, card_values):
        return self.has_royal_straight(card_values) and self.has_flush(card_suits, card_values)

    def has_straight_flush(self, card_suits, card_values):
        return self.has_straight(card_suits, card_values) and self.has_flush(card_suits, card_values)

    def has_full_house(self, card_suits, card_values):
        largest_multiple, multiples = self.get_multiples(card_values)
        return largest_multiple == 3 and len(multiples) == 2

    def has_four_of_a_kind(self, card_suits, card_values):
        largest_multiple, multiples = self.get_multiples(card_values)
        return largest_multiple == 4

    def has_three_of_a_kind(self, card_suits, card_values):
        largest_multiple, multiples = self.get_multiples(card_values)
        return largest_multiple == 3

    def has_two_pair(self, card_suits, card_values):
        largest_multiple, multiples = self.get_multiples(card_values)
        return largest_multiple == 2 and len(multiples) == 2

    def has_pair(self, card_suits, card_values):
        largest_multiple, multiples = self.get_multiples(card_values)
        return largest_multiple == 2 and len(multiples) == 1

    def has_straight(self, card_suits, card_values):
        min_card_value = min(card_values)
        return set(card_values) == set(range(min_card_value, min_card_value + 5))

    def has_royal_straight(self, card_values):
        return set(card_values) == self.ROYAL_CARD_VALUE_SET

    def has_flush(self, card_suits, card_values):
        return len(set(card_suits)) == 1

    def has_high_card(self, card_suits, card_values):
        return True

    def get_multiples(self, card_values):
        
        counter = Counter(card_values)
        max_count = 1
        multiples = set()

        for card_value, count in counter.items():
            if count >= 2:
                multiples.add(card_value)
            if count > max_count:
                max_count = count

        return max_count, multiples

class Hand:

    def __init__(self, cards):

        if len(cards) > 5:
            raise Error("")

        self.cards = cards

    def add_card(self, card):

        if len(self.cards) >= 5:
            raise Error("")
        
        self.cards.add(card)

    def get_suits(self):
        return [ card.suit for card in self.cards ]
    
    def get_values(self):
        return [ card.value for card in self.cards ]
    
    def __len__(self):
        return len(self.cards)
    
    def append(self, card):
        self.cards.append(card)

    def extend(self, cards):
        self.cards.extend(cards)

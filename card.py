from enum import Enum, IntEnum


class Suit(Enum):
    CLUBS = 'C'
    DIAMONDS = 'D'
    HEARTS = 'H'
    SPADES = 'S'

class Value(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class Card:
    
    def __init__(self, suit, value):
        
        if isinstance(suit, str):
            suit = Suit(suit)

        if isinstance(value, int):
            value = Value(value)
        
        if not isinstance(suit, Suit):
            raise Error("")
        
        if not isinstance(value, Value):
            raise Error("")
        
        self.suit = suit
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        return self.__lt__(other) or self.__eq__(other)

    def __ge__(self, other):
        return self.__gt__(other) or self.__eq__(other)

    def __str__(self):
        return str(int(self.value)) + self.suit.name

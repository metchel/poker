import unittest
from hand import Hand, HandRanker, Rank
from card import Card, Suit, Value

class TestHand(unittest.TestCase):

    def test_royal_flush(self):
        ranker = HandRanker()
        cards = [ Card('S', 14), Card('S', 13), Card('S', 12), Card('S', 11), Card('S', 10) ]
        hand = Hand(cards)
        self.assertEqual(ranker.rank(hand), Rank.ROYAL_FLUSH)

    def test_straight_flush(self):
        ranker = HandRanker()
        cards = [ Card('S', 13), Card('S', 12), Card('S', 11), Card('S', 10), Card('S', 9) ]
        hand = Hand(cards)
        self.assertEqual(ranker.rank(hand), Rank.STRAIGHT_FLUSH)

    def test_four_of_a_kind(self):
        ranker = HandRanker()
        cards = [ Card('S', 13), Card('H', 13), Card('D', 13), Card('C', 13), Card('S', 9) ]
        hand = Hand(cards)
        self.assertEqual(ranker.rank(hand), Rank.FOUR_OF_A_KIND)

    def test_full_house(self):
        ranker = HandRanker()
        cards = [ Card('S', 13), Card('H', 13), Card('D', 13), Card('C', 9), Card('S', 9) ]
        hand = Hand(cards)
        self.assertEqual(ranker.rank(hand), Rank.FULL_HOUSE)

    def test_flush(self):
        ranker = HandRanker()
        cards = [ Card('S', 13), Card('S', 12), Card('S', 11), Card('S', 3), Card('S', 9) ]
        hand = Hand(cards)
        self.assertEqual(ranker.rank(hand), Rank.FLUSH)

    def test_straight(self):
        ranker = HandRanker()
        cards = [ Card('D', 13), Card('H', 12), Card('C', 11), Card('C', 10), Card('S', 9) ]
        hand = Hand(cards)
        self.assertEqual(ranker.rank(hand), Rank.STRAIGHT)

    def test_three_of_a_kind(self):
        ranker = HandRanker()
        cards = [ Card('S', 13), Card('H', 13), Card('D', 13), Card('C', 11), Card('S', 9) ]
        hand = Hand(cards)
        self.assertEqual(ranker.rank(hand), Rank.THREE_OF_A_KIND)

    def test_two_pair(self):
        ranker = HandRanker()
        cards = [ Card('S', 13), Card('H', 13), Card('D', 12), Card('C', 9), Card('S', 9) ]
        hand = Hand(cards)
        self.assertEqual(ranker.rank(hand), Rank.TWO_PAIR)

    def test_pair(self):
        ranker = HandRanker()
        cards = [ Card('S', 13), Card('H', 13), Card('D', 12), Card('C', 3), Card('S', 9) ]
        hand = Hand(cards)
        self.assertEqual(ranker.rank(hand), Rank.PAIR)

    def test_high_card(self):
        ranker = HandRanker()
        cards = [ Card('S', 13), Card('H', 11), Card('D', 3), Card('C', 10), Card('S', 9) ]
        hand = Hand(cards)
        self.assertEqual(ranker.rank(hand), Rank.HIGH_CARD)

if __name__ == '__main__':
    unittest.main()

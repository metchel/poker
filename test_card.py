import unittest

from card import Card, Value, Suit

class TestCard(unittest.TestCase):

    def test_equality(self):
        card1 = Card(Suit.SPADES, Value.ACE)
        card2 = Card(Suit.HEARTS, Value.ACE)

        self.assertEqual(card1, card2)
    
    def test_inequailty(self):
        card1 = Card(Suit.SPADES, Value.ACE)
        card2 = Card(Suit.SPADES, Value.KING)

        self.assertNotEqual(card1, card2)

    def test_greater_than(self):
        card1 = Card(Suit.SPADES, Value.ACE)
        card2 = Card(Suit.HEARTS, Value.KING)

        self.assertTrue(card1 > card2)

    def test_greater_than_or_equal(self):
        card1 = Card(Suit.SPADES, Value.ACE)
        card2 = Card(Suit.HEARTS, Value.ACE)
        card3 = Card(Suit.SPADES, Value.KING)

        self.assertTrue(card1 >= card2)
        self.assertTrue(card1 >= card3)

if __name__ == '__main__':
    unittest.main()

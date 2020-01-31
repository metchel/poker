import unittest

from player import Player
from card import Card

class TestPlayer(unittest.TestCase):
    def test_deal(self):
        bob = Player('Bob', 300)

        ace_spades = Card('S', 14)
        queen_spades = Card('S', 12)

        bob.deal_cards([ace_spades, queen_spades])
        self.assertEqual(len(bob.hand), 2)

    def test_bet(self):

        bob = Player('Bob', 300)
        self.assertEqual(bob.cash, 300)

        bob.bet(100)
        self.assertEqual(bob.cash, 300 - 100)

    def test_fold(self):

        bob = Player('Bob', 300)
        self.assertFalse(bob.is_folded )

        bob.fold()
        self.assertTrue(bob.is_folded)

    def test_raise(self):
        bob = Player('Bob', 300)
        
        amount_raised = bob.raise_bet(100, 200)
        self.assertEqual(bob.cash, 100)
        self.assertEqual(amount_raised, 100)

if __name__ == '__main__':
    unittest.main()

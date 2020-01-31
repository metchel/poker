import unittest

from deck import Deck

class TestDeck(unittest.TestCase):
    def test_creation(self):
        the_deck = Deck()
        self.assertEqual(len(the_deck.cards), 52)

if __name__ == '__main__':
    unittest.main()

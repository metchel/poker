from card import Card
import random

class Deck:
    def __init__(self):
        self.cards = []

        for suit in ['S', 'H', 'D', 'C']:
            for value in range(2, 15):
                card = Card(suit, value)
                self.cards.append(card)

        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, players):
        if len(players) > 21:
            raise Error("")

        for _ in range(2):
            for player in players:
                card = self.cards.pop(0)
                player.deal_card(card)
    
    def flop(self, players, burn = True):
        if burn:
            self.burn_card()
        flop = []
        for _ in range(3):
            card = self.cards.pop(0)
            flop.append(card)
        
        for player in players:
            player.deal_cards(flop)

        return flop

    def river(self, players, burn = True):
        if burn:
            self.burn_card()

        river = self.cards.pop(0)
        for player in players:
            player.deal_card(river)

        return river

    def turn(self, players, burn = True):
        if burn:
            self.burn_card()

        turn = self.cards.pop(0)
        for player in players:
            player.deal_card(turn)

        return turn

    def burn_card(self):
        self.cards.pop(0)

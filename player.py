from hand import Hand

class Player:
    
    def __init__(self, name, cash):
        self.name = name
        self.hand = Hand([])
        self.cash = cash
        self.is_folded = False
        self.is_all_in = False
        self.is_out = False

    def bet(self, amount):
        if amount <= self.cash:
            self.update_cash(-1 * amount)
        else:
            raise Error("Could not make the bet.")

        if self.cash == 0:
            self.is_all_in = True

        return amount

    def call(self, amount):
        self.bet(amount)
        return amount

    def raise_bet(self, starting_amount, ending_amount):
        self.bet(ending_amount)
        return ending_amount - starting_amount

    def check(self):
        return 0

    def fold(self):
        self.is_folded = True
        return 0

    def deal_card(self, card):
        self.hand.append(card)

    def deal_cards(self, cards):
        self.hand.extend(cards)

    def update_cash(self, amount):
        if self.is_all_in and amount == 0:
            self.is_out = True

        self.cash += amount

        if self.cash == 0:
            self.all_in = True
    
    def reset(self):
        self.cards = []
        self.is_folded = False

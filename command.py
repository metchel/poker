from enum import Enum

class CommandTypes(Enum):
    BET = ('bet', 1)
    CALL = ('call', 1)
    FOLD = ('fold', 0)
    RAISE = ('raise', 2)
    CHECK = ('check', 0)

class Command:
    
    def __init__(self, name, args):
        try:
            self.command_type = CommandTypes((name, len(args)))
        except:
            print('Invalid Command')
            raise

        self.name = name
        self.args = args

        self.command_switcher = {
                CommandTypes.BET: self.bet,
                CommandTypes.CALL: self.call,
                CommandTypes.CHECK: self.check,
                CommandTypes.FOLD: self.fold,
                CommandTypes.RAISE: self.raise_bet
                }

    def execute(self, player):
        return self.command_switcher[self.command_type](player)

    def bet(self, player):
        return player.bet(self.args[0])

    def call(self, player):
        return player.call(self.args[0])

    def check(self, player):
        return player.check()

    def fold(self, player):
        return player.fold()

    def raise_bet(self, player):
        return player.raise_bet(self.args[0], self.args[1])

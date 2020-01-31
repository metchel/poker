from enum import IntEnum
from itertools import cycle

from event_stream import EventStream
from command import Command
from deck import Deck
from player import Player
from hand import Hand, HandRanker

class GameStates(IntEnum):
    BEGIN = 0
    START_ROUND = 1
    DEALING = 2
    FIRST_BET = 3
    FLOP = 4
    SECOND_BET = 5
    RIVER = 6
    THIRD_BET = 7
    TURN = 8
    LAST_BET = 9
    END_ROUND = 10
    DONE = 11

class Game:

    def __init__(self, players, event_stream):
        self.state = GameStates.BEGIN

        if len(players) < 2:
            raise Error("")

        self.players = players
        self.event_stream = event_stream

        self.transition = {
                GameStates.BEGIN: GameStates.START_ROUND,
                GameStates.START_ROUND: GameStates.DEALING,
                GameStates.DEALING: GameStates.FIRST_BET,
                GameStates.FIRST_BET: GameStates.FLOP,
                GameStates.FLOP: GameStates.SECOND_BET,
                GameStates.SECOND_BET: GameStates.RIVER,
                GameStates.RIVER: GameStates.THIRD_BET,
                GameStates.THIRD_BET: GameStates.TURN,
                GameStates.TURN: GameStates.LAST_BET,
                GameStates.LAST_BET: GameStates.END_ROUND,
                GameStates.END_ROUND: GameStates.START_ROUND }
        
        self.state_action = {
                GameStates.START_ROUND: self.start_round,
                GameStates.DEALING: self.deal,
                GameStates.FIRST_BET: self.first_bet,
                GameStates.FLOP: self.flop,
                GameStates.SECOND_BET: self.second_bet,
                GameStates.RIVER: self.river,
                GameStates.THIRD_BET: self.third_bet,
                GameStates.TURN: self.turn,
                GameStates.LAST_BET: self.last_bet,
                GameStates.END_ROUND: self.end_round,
                GameStates.DONE: self.end_game }

        self.player_turn = self.players[0]
        self.player_consensus = 0
        self.pot = 0
        self.hand_ranker = HandRanker()

    def add_player(self, player):
        self.players.append(player)
    
    def run(self):

        self.event_stream.subscribe(self)
        self.state = GameStates.START_ROUND

    def on_event(self, event):
        try:
            self.process(event['command'], event['player'])
            
            if self.player_consensus == len(self.players_in_round):
                self.next_state()
                self.player_consensus = 0

            print(player.cash)
        except:
            raise Error("something went wrong")

    def process(self, command, player):
        
        if player is not self.player_turn:
            raise Error("Not your turn!")
        
        self.pot += command.execute(player)
        
        if command.name == 'fold':
            self.players_in_round.remove(player)
            self.player_pool = cycle(self.players_in_round)

        else:
            if command.name not in [ 'raise', 'bet' ]:
                self.player_consensus += 1
            else:
                self.player_consensus = 1

    def next_state(self):
        self.state = self.transition[self.state]
        print(self.state)

    def next_turn(self):
        self.player_turn = next(self.player_pool)

    def start_round(self):
        self.deck = Deck()
        self.deck.shuffle()
        for player in self.players:
            player.hand = Hand([])

        self.players_in_round = self.players
        self.player_pool = cycle(self.players)
        self.pot = 0

        self.next_state()

    def deal(self):
        self.deck.deal(self.players)
        self.next_state()

    def first_bet(self):
        pass

    def flop(self):
        self.deck.flop(self.players)
        self.next_state()

    def second_bet(self):
        pass

    def river(self):
        self.deck.river(self.players)
        self.next_state()

    def third_bet(self):
        pass

    def turn(self):
        self.deck.turn(self.players)
        self.next_state()

    def last_bet(self):
        pass

    def end_round(self):
        min_rank = float('inf')
        min_rank_players = []

        for player in self.players_in_round:
            rank, hand = self.hand_ranker.rank(player.hand)
            player.hand = hand
            if rank == min_rank:
                min_rank_players.append(player)
            if rank < min_rank:
                min_rank = rank
                min_rank_players = [ player ]

        winner = None

        if len(min_rank_players) > 1:
            winner = self.hand_ranker.tiebrake([ p.hand for p in min_rank_players ])
        else:
            winner = min_rank_players[0]
        self.next_state()

        print("Winner is {}, with a pot of {}!!".format(winner.name, self.pot))

        winner.update_cash(self.pot)
    
    def end_game(self):
        pass

if __name__ == '__main__':
    print("Please enter the number of players: ")
    num_players = int(input())

    print("And how much is the buy in? ")
    cash = int(input())
    print("Please enter {} player names, hitting return after each name.".format(num_players))
    
    players = []
    
    for _ in range(num_players):
        player_name = input()
        player = Player(player_name, cash)
        players.append(player)

    events = EventStream()
    game = Game(players, events)
    game.run()

    while game.state != GameStates.DONE:

        if int(game.state) in [3, 5, 7, 9]: 
            print("Player {}'s turn".format(game.player_turn.name))
            print([ str(card) for card in game.player_turn.hand.cards ])
            raw_command = input()
            tokens = raw_command.split()
            command_name = tokens[0]
            args = []

            if len(tokens) > 1:
                args = tokens[1:]

            args = [ int(a) for a in args ]

            command = Command(command_name, args)

            events.publish({ 'command': command, 'player': game.player_turn })
        
        game.state_action[game.state]()
        game.next_turn()


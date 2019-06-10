from .card_deck import PlayingCardDeck
from .player import BlackJackPlayer, BlackJackDealer
from .exceptions import GameException

class BlackJackGame():

    def __init__(self,id,num_decks=1):
        self.id = id
        self.players = {}
        self.dealer = BlackJackDealer()
        self.deck = PlayingCardDeck(num_decks)
        self.pool = 0
        self.bets = {}

    def add_players(self,*args):
        for player in args:
            self.players[player.get_name()] = player

    def get_players(self):
        return self.players

    def add_deck(self,deck):
        self.shoe.extend(deck)

    def get_deck(self):
        return self.deck

    def get_bets(self):
        raise NotImplementedError()

    def deal_card_player(self,player,card):
        self.get_players()[player].give_card(card)

    def deal_initial_hand(self):
        for player in self.get_players():
            self.deal_card_player(player,self.deck.draw())

    def get_bets(self,**kwargs):
        assert len(kwargs) == len(self.get_players()), 'get_bets: Conflicting arg/players count'

        for player,bet in kwargs.items():
            self.players[player].take_chips(bet)
            self.bets[player] = bet

    def next_round(self):
        for name in self.get_players():
            print('({}: {})'.format(name,self.get_players()[name]))

            # The user interface will need to be laid out a bit more before this can be built out
            pass

    # This is responsible for running the game
    def main(self):

        # Initialize the game
        p1 = BlackJackPlayer('name1',50)
        p2 = BlackJackPlayer('name2',50)
        self.add_players(p1,p2)

        # Make bets
        self.get_bets(name1=10,name2=20)

        # Deal the hands
        self.deal_initial_hand()
        self.deal_initial_hand()
        print('Players: {}'.format(game.get_players()))
        for player in self.get_players():
            print('{}: count {}'.format(player, self.get_players()[player].get_chip_count()))

        # Check for next move
        self.next_round()

game = BlackJackGame(101,2)

game.main()
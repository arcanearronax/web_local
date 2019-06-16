from .card import PlayingCard
from ..exceptions import HandException

class AbstractHand(list):
    _card_class = None
    _card_limit = None

    def __init__(self):
        super().__init__()

    def add_card(self,card):
        assert self.get_card_count() < self._card_limit, 'Hand is at limit'
        self._cards.append(card)

    def get_card(self,ind=0):
        try:
            return self[ind]
        except IndexError:
            raise HandException('Hand index is invalid')

    def get_cards(self):
        return self[:]

    def give_card(self,card):
        assert self.get_card_count() <= self.__class__._card_limit, 'Hand is at limit'
        self.append(card)

    def give_cards(self,*args,**kwargs):
        assert self.get_card_count() + len(args) <= self.__class__._card_limit, 'Too many cards'
        for card in args:
            self.give_card(card)

    def take_card(self,ind=0):
        try:
            card = self.get_card(ind=ind)
        except IndexError:
            raise HandException('Card index does not exist')
        del self[ind]
        return card

    def take_cards(self):
        cards = self.get_cards()
        del self[:]
        return cards

    def get_card_count(self):
        return len(self)


class PlayingCardHand(AbstractHand):
    _card_class = PlayingCard
    _card_limit = 5

    def get_value(self):
        return sum(x.get_value() for x in self.get_cards())

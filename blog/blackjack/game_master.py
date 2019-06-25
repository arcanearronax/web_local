from .game import BlackJackGame
from .game_action import GameAction
from .exceptions import GameException,MasterException
import logging

logger = logging.getLogger('blog.blackjack.game_view')

# May want to end up having this extend dict
class GameMaster():
    _game_class = BlackJackGame
    games = dict()

    # Simply add a new game object to the games dict
    @classmethod
    def create_game(cls,action):
        logger.debug('ENTER: create_game')
        game_id = str(int(action.game_id))
        try:
            cls.games[game_id] = cls._game_class()
        except Exception as e:
            loggger.debug('create_game_error: {}'.format(e))
            action.error = 'e'
        else:
            success = 'Created Game {}'.format(game_id)
            logger.debug('create_game: {}'.format(success))
            action.add_note(success)
        return action

    @classmethod
    def create_player(cls,action):
        logger.debug('ENTER: create_player')
        game_id = str(int(action.game_id))
        try:
            game = cls.games[game_id]
            game.add_player(action.player_name,action.chips)
        except Exception as e:
            loggger.debug('create_player_error: {}'.format(e))
            action.add_error(e)
        else:
            success = '{} added to game {}'.format(action.player_name,game_id)
            logger.debug('create_player: {}'.format(success))
            action.add_note(success)

    @classmethod
    def start_round(cls,action):
        logger.debug('ENTER: start_round')
        game_id = str(int(action.game_id))
        try:
            game = cls.games[game_id]
            player_name = game.get_player(action.player_name).get_name()
            game.add_bet(player_name,action.chips)
            game.deal_initial_hand()
        except Exception as e:
            logger.debug('start_round_error: {}'.format(e))
            action.add_error(e)
        else:
            action.dealer_hand = game.get_dealer_cards()
            action.hands = game.get_cards(player_name)

            success = '{} dealt: {}'.format(player_name,action.hands)
            logger.debug('start_round: {}'.format(success))
            action.add_note(success)

    @classmethod
    def player_move(cls,action):
        logger.debug('ENTER: player_move')
        game_id = str(int(action.game_id))

        try:
            game = cls.games[game_id]
            player_name = action.player_name
            game.process_move(player_name,action.move)
        except Exception as e:
            logger.debug('player_move_error: {}'.format(e))
            action.error = e
            action.notes = e

        end_hand = False

        if action.move == 'stay':
            end_hand = True
        elif not game.get_player(player_name).can_move():
            end_hand = True


        if end_hand:
            logger.debug('PLAYER NOT MOVING')
            game.dealer_move()
            game.evaluate_winners()
            game.payout_bets()

            logger.debug('ACTION-WINNERS: {}'.format(game.winners))
            if game.is_simple_winner(player_name):
                action.notes = 'Player won'
            else:
                action.notes = 'Dealer won'

            action.hands = game.get_cards(player_name)
            action.dealer_hand = game.get_dealer_cards()
            game.collect_cards()
        else:
            action.hands = game.get_cards(player_name)
            action.dealer_hand = game.get_dealer_cards()

    _phase_router = {
        'create_game': create_game,
        'create_player': create_player,
        'start_round': start_round,
        'player_move': player_move,
    }

    #######################
    ## Action Processing ##
    #######################

    # Use this to comunicate with the view set
    @classmethod
    def process_action(cls,action):
        logger.debug('PROCESS ACTION: {}'.format(action.__dict__))
        if action.phase in cls._phase_router:
            eval('cls.{}(action)'.format(action.phase))
        else:
            action.notes = 'ACTION NOT FOUND'
        return action

import random
import time
from collections import deque

from attrs import Bid
from players import ComputerPlayer, HumanPlayer


class Game:
    available_computer_players_names = ['Random', 'Lucky', 'Gambler', 'SteadyHand', 'TheStableGuy']
    turn = 0

    def __init__(self):
        self.initial_players_count = None
        self.dices = None
        self.players = None

    def set_dice_count(self):
        while True:
            number_of_dices = input('Enter the number of dices per player (2 - 5): ')
            try:
                if int(number_of_dices) not in range(2, 7):
                    raise ValueError
                self.dices = int(number_of_dices)
                return True
            except ValueError:
                print('Please set correctly the number of dices')

    def set_players_count(self):
        while True:
            number_of_players = input('Enter the number of players (2 - 6): ')
            try:
                if int(number_of_players) not in range(2, 7):
                    raise ValueError
                self.initial_players_count = int(number_of_players)
                return True
            except ValueError:
                print('Please set correctly the number of players')

    def initialize(self):
        # Initialize the game parameters - player and count of dice per player
        if self.set_players_count() and self.set_dice_count():
            # generate players
            self.generate_players()
            return True

    def generate_players(self):
        """adds all players to the game"""
        human_player_name = input('Enter your name: ')

        human_player = HumanPlayer(name=human_player_name,
                                   number_of_dices=self.dices,
                                   total_dices=self.dices * self.initial_players_count)

        players = [human_player]

        players = players + self.generate_computer_player()

        self.players = deque(players)

    def generate_computer_player(self):
        comp_players = self.initial_players_count - 1
        players = set()
        while True:
            if len(players) == comp_players:
                break
            players.add(random.choice(self.available_computer_players_names))
        return [ComputerPlayer(
            name=comp,
            number_of_dices=self.dices,
            total_dices=self.dices * self.initial_players_count) for comp in players]

    def end_turn(self, bid, current_player, challenged_player):
        # reveal all dices
        all_dice = []
        for player in self.players:
            print(f"{player.name} has {player.cup.hand}")
            all_dice += player.cup.hand
        print()
        time.sleep(1)
        # check bit validity
        counter = bid.dice_counter(all_dice)
        quantity = bid.current_bid['count']
        face = bid.current_bid['face']
        if counter[face] >= quantity:
            challenged_player.win()
            current_player.loose()
        else:
            challenged_player.loose()
            current_player.win()
            self.players.rotate()
        print()
        time.sleep(1)
        # print how many dices players have
        for player in self.players:
            print(f'{player.name} has {player.cup.number_of_dices} dice(s).')
        print()

        # reset the bid
        bid.current_bid = None
        bid.last_bid = None

        # roll all dice
        for player in self.players:
            player.cup.roll()

        # increase the count of the turns
        self.turn += 1
        time.sleep(2)

    def play(self):
        print('Welcome to Liar\'s Dice. Let\'s play a game')
        if self.initialize():
            bid = Bid(self.dices * self.initial_players_count)
            while True:
                current_player = self.players[0]
                # check if is playing and if not -> pop out
                if not current_player.is_playing:
                    self.players.popleft()
                    current_player = self.players[0]

                # check for winner
                if len(self.players) == 1:
                    print(f'The Winner is ---{current_player.name}---')
                    user_input = input('Another game? (y/n): ')
                    if user_input.lower() == 'y':
                        self.play()
                    else:
                        raise SystemExit

                result = current_player.take_turn(bid)
                if result:
                    challenged_player = self.players[-1]
                    self.end_turn(bid, current_player, challenged_player)
                    continue
                self.players.rotate(-1)


if __name__ == '__main__':
    game = Game()
    game.play()

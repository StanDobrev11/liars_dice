import random
import time
from collections import deque

from players import ComputerPlayer


class Game:
    available_computer_players_names = ['Random', 'Lucky', 'Gambler']
    turn = 0

    def __init__(self):
        self.initial_players_count = None
        self.dices = None
        self.players = []

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

    def generate_players(self):
        """adds all players to the game"""
        human_player_name = input('Enter your name: ')
        # TODO class human player
        players = [human_player_name]

        players = players + self.generate_computer_player()

        self.players = players.copy()

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

    def play(self):
        print('Welcome to Liar\'s Dice. Let\'s play a game')
        # time.sleep(1)
        self.initialize()


if __name__ == '__main__':
    game = Game()
    game.play()

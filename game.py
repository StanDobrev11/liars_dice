import random
import time
from collections import deque

from attrs import Bid
from players import ComputerPlayer, HumanPlayer, BasePlayer


class Game:

    turn = 0
    available_computer_players_names = [
        "Cap'n Scattershot",
        "One-Eyed Fortune",
        "Blackjack Blackbeard",
        "Ironhook Steady",
        "Barnacle Bill the Unshaken",
    ]

    def __init__(self):
        self.initial_players_count = None
        self.dices = None
        self.players = None
        self.is_wild = False

    def set_dice_count(self):
        while True:
            number_of_dices = input(
                "How many bones be ye rattlin’, ye swashbuckler? Choose yer dice and let’s get rollin'! (2 - 5): ")
            try:
                if int(number_of_dices) not in range(2, 7):
                    raise ValueError
                self.dices = int(number_of_dices)
                return True
            except ValueError:
                print("Arrr, set the number o' dice properly, or ye'll be swabbin' the decks!")

    def set_players_count(self):
        while True:
            number_of_players = input('Arrr, how many scallywags be joinin\' this here game o\' dice, matey? (2 - 6): ')
            try:
                if int(number_of_players) not in range(2, 7):
                    raise ValueError
                self.initial_players_count = int(number_of_players)
                return True
            except ValueError:
                print("Ye best set the right number o' players, or ye’ll be walkin’ the plank!")

    def initialize(self):
        # Ask to play regular or wild version
        while True:
            user_input = input("Arrr! Do ye want to play regular or wild, matey? (R/W): ")
            if user_input.lower().strip() == 'r':
                break
            elif user_input.lower().strip() == 'w':
                self.is_wild = True
                BasePlayer.is_wild = True
                break
            else:
                print("Arrr, make a proper choice, ye scallywag, or ye'll be feedin' the sharks!")

        # Initialize the game parameters - player and count of dice per player
        if self.set_players_count() and self.set_dice_count():
            # generate players
            self.generate_players()
            return True

    def generate_players(self):
        """adds all players to the game"""
        human_player_name = input("Arrr, tell us yer name, ye salty sea dog: ")

        human_player = HumanPlayer(name=human_player_name,
                                   number_of_dices=self.dices)

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
            number_of_dices=self.dices) for comp in players]

    def end_turn(self, bid, current_player, challenged_player):
        # reveal all dices
        all_dice = []
        for player in self.players:
            print(f"Arrr, {player.name} be holdin' {player.cup.hand} in their hand!")
            all_dice += player.cup.hand
        print()
        time.sleep(1)

        quantity = bid.current_bid['count']
        face = bid.current_bid['face']

        counter = bid.dice_counter(all_dice)
        # account for the wild version to produce correct count of the dices
        if self.is_wild and face != 1:
            counter[face] += counter[1]

        if counter[face] >= quantity:
            challenged_player.win()
            current_player.loose(bid)
        else:
            challenged_player.loose(bid)
            current_player.win()
            self.players.rotate()
        print()
        time.sleep(1)
        # print how many dices players have
        for player in self.players:
            print(f"Avast! {player.name} be havin' {player.cup.number_of_dices} dice(s) in their cup!")
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
        print("Welcome aboard to Liar's Dice! Let’s be havin’ ourselves a game, ye scurvy lot!")
        if self.initialize():
            bid = Bid(self.dices * self.initial_players_count)
            while True:
                current_player = self.players[0]
                # set total dices for each player
                current_player.total_dices = bid.total_dices

                # check if is playing and if not -> pop out
                if not current_player.is_playing:
                    self.players.popleft()
                    current_player = self.players[0]

                # check for winner
                if len(self.players) == 1:
                    print(
                        f"Hoist the colors! The winner be ---{current_player.name}---, the mightiest pirate o' them all!")
                    user_input = input("Fancy another round, matey? (y/n): ")
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

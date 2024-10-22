import random
import math
from collections import deque


class Dice:
    def __init__(self):
        self._face = None

    @property
    def face(self):
        return self._face

    def roll(self):
        self._face = random.randint(1, 6)
        return self.face

    def __repr__(self):
        return str(self.face)


class Cup:

    def __init__(self, number_of_dices):
        self.number_of_dices = number_of_dices
        self._dices = [Dice()] * self.number_of_dices

    @property
    def hand(self):
        return self._dices

    def roll(self):
        self._dices = [dice.roll() for dice in self._dices]
        return self

    def add_dice(self):
        self.number_of_dices += 1
        self._dices.append(Dice())

    def remove_dice(self):
        self.number_of_dices += 1
        self._dices.remove(Dice())
        if self.number_of_dices == 0:
            return False
        return True

    def __str__(self):
        return f'{[dice for dice in self.hand]}'


class Bid:
    current_player = None

    def __init__(self, total_dices):
        self.total_dices = total_dices
        self.last_bid = None
        self.current_bid = None

    def check_bid_validity(self, count, face):

        if self.current_bid is None:
            self.current_bid = {}
        else:
            self.last_bid = self.current_bid

        try:
            if count >= self.total_dices or count <= 0:
                raise ValueError('Count cannot be zero or negative or bigger that the total number of dices.')

            if face not in range(1, 7):
                raise ValueError("Face must be between 1 and 6.")

            if count <= self.last_bid['count'] and face <= self.last_bid['face']:
                raise ValueError('Please place a proper bid.')

        except ValueError as v:
            print(v)
            return False

        except TypeError:
            return True

        except KeyError:
            return True

        return True

    @classmethod
    def dice_counter(cls, dices):
        counter = {}

        for face in range(1, 7):
            counter[face] = dices.count(face)

        return counter

    def place_bid(self, count, face, player):
        # check if the bid is valid and set the current bid
        if self.check_bid_validity(count, face):
            self.current_bid['count'] = count
            self.current_bid['face'] = face
            self.current_player = player

    def __str__(self):
        return f"The current bid is:\n Count: {self.current_bid['count']}\n Face: {self.current_bid['face']}'s"


class ComputerPlayer:
    def __init__(self, name, number_of_dices, total_dices):
        self.cup = Cup(number_of_dices).roll()
        self.name = name
        self.is_playing = True
        self.gambler_threshold = 0.3
        self.total_dices = total_dices

    def place_bid(self, bid, count, face):
        result = bid.place_bid(count, face, self)

        if result:
            return result, False

        return f"{self.name} placed a bid.\n{bid}", True

    def generate_combinations(self, bid):
        # extract the current bid values
        bid_quantity, bid_face = self.extract_quantity_face([bid])

        # increase the face, increase the quantity
        for

    def decide(self, bid):
        """calculate proba and make a decision"""

        proba = self.calculate_bid_proba(bid)

        if proba > self.gambler_threshold:
            # TODO the bid is probable so place a bid
            # generate combinations -> possible combination are face + 1, quantity + 1, face & quantity + 1
            combinations = self.generate_combinations(bid)

            # calculate probabs
            # select calculation
            pass
        else:
            # TODO challenge the player if bid not probable
            self.challenge()

    def challenge(self):
        # TODO reveal all players' hands
        # TODO calculate if the bid is matched
        # TODO decide the outcome
        pass

    @staticmethod
    def extract_quantity_face(*args):
        if len(args) == 1:
            bid = args[0]
            # get the face of the current bid
            face = bid.current_bid['face']
            quantity = bid.current_bid['count']
        else:
            quantity, face = args

        return quantity, face

    def calculate_bid_proba(self, *args, sim=10000):

        quantity, face = self.extract_quantity_face(*args)

        # extract the number of faces in the current player's cup
        face_in_cup = self.cup.hand.count(face)

        # generate the number of dices bss the current face in player's cup
        all_dice = self.total_dices - face_in_cup

        # run simulations
        valid_bid_count = 0
        for _ in range(sim):
            all_dice_rolled = [Dice().roll() for _ in range(all_dice)]

            # add the players dices
            if face_in_cup > 0:
                all_dice_rolled.extend([face] * face_in_cup)

            counter = Bid(all_dice).dice_counter(all_dice_rolled)

            # compare bid to proba
            if counter[face] >= quantity:
                valid_bid_count += 1

        return valid_bid_count / sim

    def __str__(self):
        return self.name


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

        players = players.extend(self.generate_computer_player())

        self.players = players.copy()

    def generate_computer_player(self):
        comp_players = self.initial_players_count - 1
        players = set()
        while True:
            if len(players) == comp_players:
                break
            players.add(random.choice(self.available_computer_players_names))
        return [ComputerPlayer(
            name=comp.name,
            number_of_dices=self.dices,
            total_dices=self.dices * self.initial_players_count) for comp in players]


if __name__ == '__main__':
    total_dices = 15
    current_bid = Bid(total_dices)
    player = ComputerPlayer('Ivo', 5, total_dices)
    player.place_bid(current_bid, 4, 4)
    print(player.cup)
    print(player.calculate_bid_proba(current_bid))

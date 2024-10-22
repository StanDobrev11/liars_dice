import itertools
import random
import time
from abc import ABC, abstractmethod

from items import Cup, Dice, Bid


class BasePlayer(ABC):
    """
    A base class for all players (human and computer) in the game of Liar's Dice.

    Attributes:
    - total_dices (int): Total number of dice in the game.
    - is_wild (bool): Flag indicating if the game is in wild mode (1's are wild).

    Methods:
    - decide(bid): Abstract method to make a decision for the player's turn.
    - place_bid(bid, count, face): Place a valid bid for the player.
    - challenge(): Static method to challenge the current bid by calling 'Liar!'.
    - take_turn(bid): Handles the player's turn, either placing a bid or challenging.
    - win(): Declares the player as the winner of the round.
    - lose(bid): Handles the player losing a round and losing a die.
    """
    total_dices = None
    is_wild = False

    def __init__(self, name, number_of_dices):
        self.cup = Cup(number_of_dices).roll()
        self.name = name
        self.is_playing = True

    @abstractmethod
    def decide(self, bid):
        pass

    def place_bid(self, bid, count, face):
        result = bid.place_bid(count, face, self)

        if result:
            return f"{self.name} placed a bid. Brave, but let’s see if fortune favors ye!"

        return False

    @staticmethod
    def challenge():
        return 'Liar!'

    def take_turn(self, bid):
        print(f"{bid}\n")
        result = self.decide(bid)
        print(result)
        if result == 'Liar!':
            return True
        time.sleep(1)

    def win(self):
        print(f"Arrr, {self.name} won this round, ye lucky sea rat! Fortune be smilin' on ye today!")

    def loose(self, bid):
        result = self.cup.remove_dice()
        bid.total_dices -= 1
        print(f"{self.name} lost this one, ye scurvy dog! Better luck next time, or ye’ll be walkin' the plank!")
        if not result:
            print(f"Arrr, {self.name} be out o' the game! The sea's a harsh mistress!")
            self.is_playing = False

    def __str__(self):
        return self.name


class HumanPlayer(BasePlayer):
    """
    A class representing a human player in the game of Liar's Dice.

    Methods:
    - decide(bid): Prompts the user to make a decision to place a bid or call 'Liar!'.
    """

    def decide(self, bid):
        while True:
            choice = input(
                f"Make yer choice, ye salty sea dog! Yer hand be: {self.cup.hand}\nWill ye place a bet (1) or call ‘em a liar (2)? What’ll it be? ")
            if choice == '1':
                quantity = input("How many o’ yer dice show the same face? Enter the quantity, ye sea dog: ")
                face = input("What be the value o’ the face ye be biddin' on? Speak up, ye bilge rat: ")
                try:
                    result = self.place_bid(bid, count=int(quantity), face=int(face))
                except ValueError:
                    print("Ye need to place a proper bid, or ye’ll be feedin’ the fish!")
                    continue
                if result:
                    return result

            elif choice == '2':
                if not bid.current_bid:
                    print("Arrr, there be no one to call a liar just yet! Ye best place yer bid, ye scallywag!")
                    continue
                return self.challenge()


class ComputerPlayer(BasePlayer):
    """
    A class representing a computer player in the game of Liar's Dice.

    Attributes:
    - gambler (dict): A dictionary containing different player types and their gamble thresholds.

    Methods:
    - generate_combinations(bid): Generates all possible bid combinations.
    - new_bid_count_and_face(): Generates a new bid with a random count and face.
    - decide(bid): Makes a decision to place a bid or call 'Liar!' based on probability.
    - generate_probabilities(combinations): Calculates probabilities for each bid combination.
    - extract_quantity_face(*args): Extracts the count and face from a bid or arguments.
    - calculate_bid_proba(quantity, face, sim=10000): Calculates the probability of a successful bid.
    """
    gambler = {
        "Cap'n Scattershot": 0.5,
        "One-Eyed Fortune": 0.45,
        "Blackjack Blackbeard": 0.6,
        "Ironhook Steady": 0.4,
        "Barnacle Bill the Unshaken": 0.3,
    }

    def __init__(self, name, number_of_dices):
        super().__init__(name, number_of_dices)
        self.gambler_threshold = self.gambler[name]
        self.is_computer = True

    def generate_combinations(self, bid):
        # extract the current bid values
        bid_quantity, bid_face = self.extract_quantity_face(bid)

        # for higher faces than current, all possible counts are valid
        bigger_faces = [x for x in range(bid_face + 1, 7)]
        all_quantities = [x for x in range(1, bid.total_dices + 1)]
        combinations = list(itertools.product(all_quantities, bigger_faces))

        # for the same face, only larger
        same_face = [bid_face]
        larger_quantities = [x for x in range(bid_quantity + 1, bid.total_dices + 1)]
        combinations += list(itertools.product(larger_quantities, same_face))

        return combinations

    def new_bid_count_and_face(self):
        """ calculates the new bid count and face """
        # setting face counts
        end_range = 3
        if self.cup.number_of_dices <= end_range:
            end_range = self.cup.number_of_dices - 1
            if end_range <= 0:
                end_range = 1

        quantity = random.randint(1, end_range)

        # to start lower
        face = random.randint(1, 3)

        return quantity, face

    def decide(self, bid):
        """calculate proba and make a decision"""

        if not bid.current_bid:
            quantity, face = self.new_bid_count_and_face()
            return self.place_bid(bid, quantity, face)

        quantity, face = self.extract_quantity_face(bid)

        proba = self.calculate_bid_proba(quantity, face)

        # the bid is probable so place a bid
        if proba > self.gambler_threshold:

            # generate combinations
            combinations = self.generate_combinations(bid)

            # if no combinations left, challenge the player
            if not combinations:
                return self.challenge()

            # calculate probabs
            result_proba = self.generate_probabilities(combinations)

            # select calculation bss model
            for _ in range(100):
                choice = random.choice(result_proba)
                if choice[0] > 1 - self.gambler_threshold:
                    quantity, face = choice[1]
                    return self.place_bid(bid, quantity, face)

            # if not suitable choice, then take the higher prob combination
            quantity, face = sorted(result_proba, key=lambda x: x[0], reverse=True)[0][1]
            return self.place_bid(bid, quantity, face)

        else:
            # the bit is not probable so challenge last player
            return self.challenge()

    def generate_probabilities(self, combinations):
        result_probabilities = []
        for com in combinations:
            quantity, face = com
            result = self.calculate_bid_proba(quantity, face, 1000)
            result_probabilities.append((result, com))
        return result_probabilities

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

    def calculate_bid_proba(self, quantity, face, sim=10000):

        # extract the number of faces in the current player's cup
        face_in_cup = self.cup.hand.count(face)

        # add ones to calculate proba
        if self.is_wild and face != 1:
            face_in_cup += self.cup.hand.count(1)

        # generate the number of dices bss the current face in player's cup
        all_dice = self.total_dices - face_in_cup

        # run simulations
        valid_bid_count = 0
        for _ in range(sim):
            all_dice_rolled = [Dice().roll() for _ in range(all_dice)]

            # add the players dices
            if face_in_cup > 0:
                all_dice_rolled.extend([face] * face_in_cup)

            # get the counter of the face count
            counter = Bid(all_dice).dice_counter(all_dice_rolled)

            # account for the wild version
            if self.is_wild and face != 1:
                counter[face] += counter[1]

            # compare bid to proba
            if counter[face] >= quantity:
                valid_bid_count += 1

        return valid_bid_count / sim

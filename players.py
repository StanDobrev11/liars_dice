import itertools
import random
import time
from abc import ABC, abstractmethod

from attrs import Cup, Dice, Bid


class BasePlayer(ABC):
    def __init__(self, name, number_of_dices, total_dices):
        self.cup = Cup(number_of_dices).roll()
        self.name = name
        self.total_dices = total_dices
        self.is_playing = True
        self.is_computer = False

    @abstractmethod
    def decide(self, bid):
        pass

    def place_bid(self, bid, count, face):
        result = bid.place_bid(count, face, self)

        if result:
            return f"{self.name} placed a bid.\n"

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
        # increase dice count
        self.cup.add_dice()
        print(f'{self.name} wins the round!')

    def loose(self):
        result = self.cup.remove_dice()
        print(f"{self.name} looses this round...")
        if not result:
            print(f'{self.name} is out of the game')
            self.is_playing = False

    def __str__(self):
        return self.name


class HumanPlayer(BasePlayer):

    def decide(self, bid):
        while True:
            choice = input(
                f'Please make a choice.\nYour hand is: {self.cup.hand}\nPlace a bet(1) or call them a LIAR(2): ')
            if choice == '1':
                quantity = input('Enter face quantity: ')
                face = input('Enter face value: ')
                result = self.place_bid(bid, count=int(quantity), face=int(face))
                if result:
                    return result

            elif choice == '2':
                if not bid.current_bid:
                    print('There is no one to call a LIAR yet! Place a bid!')
                    continue
                return self.challenge()


class ComputerPlayer(BasePlayer):

    gambler = {
        'Random': 0.5,
        'Lucky': 0.45,
        'Gambler': 0.6,
        'SteadyHand': 0.4,
        'TheStableGuy': 0.3
    }

    def __init__(self, name, number_of_dices, total_dices):
        super().__init__(name, number_of_dices, total_dices)
        self.gambler_threshold = self.gambler[name]
        self.is_computer = True

    def generate_combinations(self, bid):
        # Extract the current bid values
        bid_quantity, bid_face = self.extract_quantity_face(bid)

        # For higher faces than current, all possible counts are valid
        bigger_faces = [x for x in range(bid_face + 1, 7)]
        all_quantities = [x for x in range(1, bid.total_dices + 1)]
        combinations = list(itertools.product(all_quantities, bigger_faces))

        # For the same face, only larger
        same_face = [bid_face]
        larger_quantities = [x for x in range(bid_quantity + 1, bid.total_dices + 1)]
        combinations += list(itertools.product(larger_quantities, same_face))


        return combinations

    def new_bid_count_and_face(self):
        """ calculates the new bid count and face """
        quantity = random.randint(1, 3)
        face = random.randint(1, 3)

        return quantity, face

    def decide(self, bid):
        """calculate proba and make a decision"""

        if not bid.current_bid:
            quantity, face = self.new_bid_count_and_face()
            return self.place_bid(bid, quantity, face)

        quantity, face = self.extract_quantity_face(bid)

        proba = self.calculate_bid_proba(quantity, face)

        if proba > self.gambler_threshold:
            # the bid is probable so place a bid
            # generate combinations -> possible combination are face + 1, quantity + 1, face & quantity + 1
            combinations = self.generate_combinations(bid)

            # calculate probabs
            result_proba = self.generate_probabilities(combinations)

            # select calculation bss model
            for _ in range(100):
                choice = random.choice(result_proba)
                if choice[0] > 1 - self.gambler_threshold:
                    quantity, face = choice[1]
                    return self.place_bid(bid, quantity, face)

            # if not suitable choice, then take the higher
            quantity, face = sorted(result_proba, key=lambda x: x[0], reverse=True)[0][1]
            return self.place_bid(bid, quantity, face)

        else:
            return self.challenge()

    def generate_probabilities(self, combinations):
        result_probabilities = []
        for com in combinations:
            quantity, face = com
            result = self.calculate_bid_proba(quantity, face, sim=1000)
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


if __name__ == '__main__':
    player = HumanPlayer('Stan', 5, 15)
    bid = Bid(15)
    player.decide(bid)

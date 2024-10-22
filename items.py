import random


class Dice:
    """
    A class representing a single die.

    Methods:
    - roll: Rolls the die and returns the face value.
    - face: Property to access the current face value of the die.
    """

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
    """
    A class representing a cup holding multiple dice.

    Attributes:
    - number_of_dices: The total number of dice in the cup.
    - hand: A list of Dice objects representing the dice in the cup.

    Methods:
    - roll: Rolls all the dice in the cup.
    - remove_dice: Removes one die from the cup and returns False if no dice remain.
    """

    def __init__(self, number_of_dices):
        self.number_of_dices = number_of_dices
        self._dices = [Dice() for _ in range(self.number_of_dices)]

    @property
    def hand(self):
        return self._dices

    def roll(self):
        self._dices = [Dice() for _ in range(self.number_of_dices)]
        self._dices = [dice.roll() for dice in self._dices]
        return self

    def remove_dice(self):
        self.number_of_dices -= 1
        if self.number_of_dices == 0:
            return False
        return True

    def __str__(self):
        return f'{[dice for dice in self.hand]}'


class Bid:
    """
    A class representing the bidding system in the game.

    Attributes:
    - total_dices: The total number of dice in the game.
    - current_bid: The current bid in the game.
    - last_bid: The previous bid placed in the game.

    Methods:
    - check_bid_validity: Validates the bid made by a player.
    - place_bid: Places a valid bid and updates the current bid.
    - dice_counter: Counts the frequency of each dice face in a list of dice.
    """
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

            if count > self.total_dices or count <= 0:
                raise ValueError(
                    "Arrr! The count can't be zero, negative, or greater than the total number o' dice in play, ye scallywag!")

            if int(face) not in range(1, 7):
                raise ValueError("Ye face value must be between 1 and 6, matey! No foolin' around with improper faces!")

            # the player can bid any count of a higher face
            if face < self.last_bid['face']:
                # if the face is lower
                raise ValueError("Ye need to place a proper bid, or ye’ll be feedin’ the fish!")

            # the player can bid a higher count of the same face
            elif face == self.last_bid['face']:
                # the count is higher than last
                if count <= self.last_bid['count']:
                    raise ValueError("Ye need to place a proper bid, or ye’ll be feedin’ the fish!")

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

        return {face: dices.count(face) for face in range(1, 7)}

    def place_bid(self, count, face, player):
        # check if the bid is valid and set the current bid
        if self.check_bid_validity(count, face):
            self.current_bid = {'count': count, 'face': face}
            self.current_player = player
            return True

        return False

    def __str__(self):
        if self.current_bid:
            return f"\nHere be the current bid, ye landlubber:\n Count: {self.current_bid['count']}\n Face: {self.current_bid['face']}'s"
        else:
            return "\nArrr, there be no bid placed yet, matey! Make yer move!"

import random


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
        self._dices = [Dice()] * self.number_of_dices
        self._dices = [dice.roll() for dice in self._dices]
        return self

    def add_dice(self):
        self.number_of_dices += 1

    def remove_dice(self):
        self.number_of_dices -= 1
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
            isinstance(all([count, face]), int)

            if count > self.total_dices or count <= 0:
                raise ValueError('Count cannot be zero or negative or bigger that the total number of dices.')

            if int(face) not in range(1, 7):
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
            return True

        return False

    def __str__(self):
        if self.current_bid:
            return f"The current bid is:\n Count: {self.current_bid['count']}\n Face: {self.current_bid['face']}'s"
        else:
            return f"There is no placed bid yet!"
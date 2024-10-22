import itertools

from attrs import Cup, Dice, Bid


class BasePlayer:
    def __init__(self, name, number_of_dices, total_dices):
        self.cup = Cup(number_of_dices).roll()
        self.name = name
        self.total_dices = total_dices
        self.is_playing = True


class ComputerPlayer(BasePlayer):
    def __init__(self, name, number_of_dices, total_dices):
        super().__init__(name, number_of_dices, total_dices)
        self.gambler_threshold = 0.3

    def place_bid(self, bid, count, face):
        result = bid.place_bid(count, face, self)

        if result:
            return result, False

        return f"{self.name} placed a bid.\n{bid}", True

    def generate_combinations(self, bid):
        # extract the current bid values
        bid_quantity, bid_face = self.extract_quantity_face(bid)

        faces = [x for x in range(bid_face, 7)]
        quantities = [x for x in range(bid_quantity, bid.total_dices + 1)]

        combinations = list(itertools.product(quantities, faces))
        combinations.remove((bid_quantity, bid_face))

        return combinations

    def decide(self, bid):
        """calculate proba and make a decision"""

        quantity, face = self.extract_quantity_face(bid)

        proba = self.calculate_bid_proba(quantity, face)

        if proba > self.gambler_threshold:
            # the bid is probable so place a bid
            # generate combinations -> possible combination are face + 1, quantity + 1, face & quantity + 1
            combinations = self.generate_combinations(bid)

            # implement selection of combinations
            combinations = combinations[:9]

            # calculate probabs
            result_proba = self.generate_probabilities(combinations)

            # select calculation
            quantity, face = sorted(result_proba, key=lambda x: x[0], reverse=True)[0][1]

            return self.place_bid(bid, quantity, face)

        else:
            # TODO challenge the player if bid not probable
            self.challenge()

    def generate_probabilities(self, combinations):
        result_probabilities = []
        for com in combinations:
            quantity, face = com
            result = self.calculate_bid_proba(quantity, face, sim=1000)
            result_probabilities.append((result, com))
        return result_probabilities

    def challenge(self):
        # TODO end turn
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

    def __str__(self):
        return self.name

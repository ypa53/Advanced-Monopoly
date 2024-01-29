import random
class Dice:
    def __init__(self):
        self.double_count = 0

    @staticmethod
    def roll_dice():
        dice = random.randint(1, 6)
        return dice




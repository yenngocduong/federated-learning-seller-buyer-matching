import random
from config import Config


class Seller(object):
    def __init__(self, i, ask=None):
        self.num = int(i)
        ask_up = Config.ask_up
        ask_low = Config.ask_low
        if ask is None:
            self.ask = Ask(i, random.randint(ask_low, ask_up))
        else:
            self.ask = ask
        self.buyer = 0

    def get_ask(self):
        return self.ask


class Ask(object):
    def __init__(self, i, ask):
        self.num = i
        self.ask = ask
        self.reward = 0

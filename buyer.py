import random
from config import Config


class Buyer(object):
    def __init__(self, i, m, bids=None, budget=None):
        self.num = int(i)
        budget_up = Config.budget_up
        budget_low = Config.budget_low
        bid_up = Config.bid_up
        bid_low = Config.bid_low
        if bids is None:
            self.bids = [Bid(i, j, random.randint(bid_low, bid_up)) for j in range(m)]
        else:
            self.bids = bids
        if budget is None:
            self.budget = random.randint(budget_low, budget_up)
        else:
            self.budget = budget

    def get_bids(self):
        return self.bids

    def get_budget(self):
        return self.budget


class Bid(object):
    def __init__(self, i, j, bid):
        self.buyer = i
        self.seller = j
        self.bid = bid
        self.payment = 0

from datetime import datetime

from entities.bid import Bid
from entities.event import Event
from entities.member import Member


class BidWinner:
    def __init__(self, event: Event, winner: Member, lowest_bid: Bid):
        self.event = event
        self.winner = winner
        self.lowest_bid = lowest_bid
        self.winning_date = datetime.now()

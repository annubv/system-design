from datetime import datetime
from optparse import Option
from typing import List, Optional

from entities.bid import Bid
from enums.event_status import EventStatus
from exceptions.exceptions import InvalidEventException


class Event:
    def __init__(self, event_id: str, name: str, prize: str, date: datetime.date):
        self.id = event_id
        self.name = name
        self.prize = prize
        self.date = date
        self.bids: List[Bid] = []
        self.event_status = EventStatus.LIVE
        self.lowest_bid: Optional[Bid] = None

    def end_event(self):
        self.event_status = EventStatus.ENDED

    def add_bid(self, bids: List[Bid]):
        if self.event_status != EventStatus.LIVE:
            raise InvalidEventException(f"Event: {self.name} is not live anymore!")

        for bid in bids:
            if not self.lowest_bid:
                self.lowest_bid = bid
            elif bid.bid_value < self.lowest_bid.bid_value:
                self.lowest_bid = bid
            self.bids.append(bid)

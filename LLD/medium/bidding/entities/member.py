from typing import List

from constants.constants import Constants
from exceptions.exceptions import InvalidMemberEventException, DuplicateMemberEventException


class Member:
    def __init__(self, member_id: str, name: str, super_coins: int):
        self.id = member_id
        self.name = name
        self.super_coins = super_coins
        self.registered_events = set()
        self.bid_events = set()

    def register_event(self, event_id: str):
        if event_id in self.registered_events:
            raise DuplicateMemberEventException(f"{self.name} already registered for the event: {event_id}.")
        self.registered_events.add(event_id)

    def submit_bid(self, event_id: str, bids: List[int]):
        if event_id not in self.registered_events:
            raise InvalidMemberEventException("Member did not register for this event")

        if event_id in self.bid_events:
            raise InvalidMemberEventException("Member has already bid this event")

        if len(bids) > Constants.MAX_BIDS_ALLOWED_PER_USER:
            raise ValueError(f"You can submit at most {Constants.MAX_BIDS_ALLOWED_PER_USER} bids.")

        if len(set(bids)) != len(bids):
            raise ValueError("Bids must be unique.")

        if any(bid <= 0 for bid in bids):
            raise ValueError("Bids must be greater than zero.")

        max_bid = max(bids)
        if self.super_coins < max_bid:
            raise ValueError(f"{self.name} doesn't have enough super coins.")

        self.super_coins -= max_bid
        self.bid_events.add(event_id)
        return bids

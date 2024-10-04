from datetime import datetime
from typing import Dict, List, Set

from constants.constants import Constants
from entities.bid import Bid
from entities.bid_winner import BidWinner
from entities.event import Event
from entities.member import Member
from enums.event_status import EventStatus
from exceptions.exceptions import SingletonInitException, DuplicateMemberException, DuplicateEventException, \
    InvalidMemberException, InvalidEventException, NoBidsException, InvalidSortingException, InvalidCommandException
from utils.utils import Utils


class BidService:
    _instance = None

    def __init__(self):
        if BidService._instance is not None:
            raise SingletonInitException("This is a singleton class")
        else:
            BidService._instance = self
            self.events: Dict[str, Event] = {}
            self.event_names: Set[str] = set()
            self.event_dates: Set[datetime.date] = set()
            self.members: Dict[str, Member] = {}
            self.past_winners: List[BidWinner] = []

    @staticmethod
    def get_instance():
        if BidService._instance is None:
            return BidService()
        else:
            return BidService._instance

    def add_member(self, member_id: str, name: str, super_coins: int):
        if member_id in self.members:
            raise DuplicateMemberException(f"A member with id: {member_id} already exists.")

        new_member = Member(member_id=member_id, name=name, super_coins=super_coins)
        self.members[member_id] = new_member
        print(f"{new_member.name} added successfully ")

    def __save_event(self, event: Event):
        self.events[event.id] = event
        self.event_dates.add(event.date)
        self.event_names.add(event.name)

    def add_event(self, event_id: str, name: str, prize: str, date: str):
        if not Utils.represents_date(date):
            raise InvalidCommandException("Invalid Date. The correct format is: YYYY-MM-DD")

        date = Utils.str_to_date(date)
        if event_id in self.events:
            raise DuplicateEventException(f"Event with id: {event_id} already exists.")

        if name in self.event_names:
            raise DuplicateEventException(f"Event with name: {name} already exists.")

        if date in self.event_dates:
            raise DuplicateEventException(f"Event with date: {date} already exists.")

        new_event = Event(event_id=event_id, name=name, prize=prize, date=date)
        self.__save_event(event=new_event)
        print(f"{new_event.name} with prize {new_event.prize} added successfully")

    def __validate_member(self, member_id: str):
        if member_id not in self.members:
            raise InvalidMemberException(f"Member with id {member_id} does not exist.")

    def __validate_event(self, event_id: str):
        if event_id not in self.events:
            raise InvalidEventException(f"Event with id {event_id} does not exist.")

        event = self.events[event_id]
        if event.event_status != EventStatus.LIVE:
            raise InvalidEventException(f"Event: {event.name} is not live anymore.")

    def register_member(self, member_id: str, event_id: str):
        self.__validate_member(member_id=member_id)
        self.__validate_event(event_id=event_id)
        self.members[member_id].register_event(event_id)
        print(f"{self.members[member_id].name} registered to the {self.events[event_id].name} event successfully")

    def submit_bid(self, member_id: str, event_id: str, bid_values: List[int]):
        self.__validate_member(member_id=member_id)
        self.__validate_event(event_id=event_id)
        member = self.members[member_id]
        event = self.events[event_id]

        member.submit_bid(event_id=event_id, bids=bid_values)
        bid_instances = [Bid(member_id=member_id, bid_value=bid) for bid in bid_values]
        event.add_bid(bids=bid_instances)
        print("BIDS submitted successfully")

    def declare_winner(self, event_id):
        self.__validate_event(event_id=event_id)
        event = self.events[event_id]
        lowest_bid = event.lowest_bid
        if not lowest_bid:
            raise NoBidsException("No bids for this event.")

        winner_id = lowest_bid.member_id
        winner = self.members[winner_id]

        bid_winner = BidWinner(event=event, winner=winner, lowest_bid=lowest_bid)
        self.past_winners.append(bid_winner)

        print(
            f"{winner.name} wins the {event.prize} with lowest bid {lowest_bid.bid_value}."
        )

    def __sort_winners(self, criteria="date", order_by="asc"):
        if order_by not in ("asc", "desc"):
            raise InvalidSortingException(f"Unsupported sorting order_by: {order_by}")

        reverse_sort = order_by == "desc"

        if criteria == "date":
            return sorted(self.past_winners, key=lambda x: x.event.date, reverse=reverse_sort)
        elif criteria == "bid_value":
            return sorted(self.past_winners, key=lambda x: x.lowest_bid.bid_value, reverse=reverse_sort)
        else:
            raise InvalidSortingException(f"Unsupported sorting criteria: {criteria}")

    def list_winners(self, order_by="asc", criteria="date"):
        if len(self.past_winners) == 0:
            print("No past winners.")
            return

        sorted_winners = self.__sort_winners(criteria, order_by)
        winners_result = []
        total_winners = min(Constants.MAX_WINNERS_TO_DISPLAY, len(sorted_winners))
        for winner_idx in range(total_winners):
            each_winner = sorted_winners[winner_idx]
            winners_result.append((each_winner.event.id, each_winner.winner.name, each_winner.lowest_bid.bid_value,
                                   Utils.date_to_str(each_winner.event.date)))
        print(winners_result)

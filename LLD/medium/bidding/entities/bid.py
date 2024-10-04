from datetime import datetime


class Bid:
    def __init__(self, member_id: str, bid_value: int):
        self.member_id = member_id
        self.bid_value = bid_value
        self.bid_time = datetime.now()

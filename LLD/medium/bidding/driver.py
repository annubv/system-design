from services.bid_service import BidService


class BiddingDriver:
    @staticmethod
    def run():
        bid_blitz = BidService()

        # Adding Members
        bid_blitz.add_member('1', "Adam", 10000)
        bid_blitz.add_member('2', "Chris", 5000)

        # Adding Event
        bid_blitz.add_event('1', "BBD", "IPHONE-14", "2023-06-06")

        # Register Members
        bid_blitz.register_member('1', '1')
        bid_blitz.register_member('2', '1')

        # Submit Bids
        bid_blitz.submit_bid('1', '1', [100, 200, 300, 400, 500])
        bid_blitz.submit_bid('2', '1', [150, 250, 350, 450])

        # Declare Winner
        bid_blitz.declare_winner(1)

        # List Winners
        bid_blitz.list_winners('asc')


if __name__ == "__main__":
    BiddingDriver.run()

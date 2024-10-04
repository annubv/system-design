from exceptions.exceptions import InvalidCommandException
from services.bid_service import BidService
from utils.utils import Utils


class BiddingCli:
    @staticmethod
    def run():
        system = BidService()

        while True:
            try:
                command = input().strip().split()
                if len(command) == 0:
                    raise InvalidCommandException("Invalid command")

                if command[0] == "ADD_MEMBER":
                    if len(command) != 4:
                        raise InvalidCommandException(
                            "Invalid ADD_MEMBER command. The syntax is: ADD_MEMBER <member_id> <member_name> <super_coins>"
                        )

                    member_id = command[1]
                    name = command[2]
                    super_coins = command[3]

                    if not Utils.represents_int(super_coins):
                        raise InvalidCommandException("Invalid super coins value")

                    super_coins = int(super_coins)
                    system.add_member(member_id, name, super_coins)

                elif command[0] == "ADD_EVENT":
                    if len(command) != 5:
                        raise InvalidCommandException(
                            "Invalid ADD_EVENT command. The syntax is: ADD_EVENT <event_id> <event_name> <prize_name> <date:YYYY-MM-DD>"
                        )
                    event_id = command[1]
                    name = command[2]
                    prize = command[3]
                    date = command[4]
                    system.add_event(event_id, name, prize, date)

                elif command[0] == "REGISTER_MEMBER":
                    if len(command) != 3:
                        raise InvalidCommandException(
                            "Invalid REGISTER_MEMBER command. The syntax is: REGISTER_MEMBER <member_id> <event_id>"
                        )
                    member_id = command[1]
                    event_id = command[2]
                    system.register_member(member_id, event_id)
                    pass

                elif command[0] == "SUBMIT_BID":
                    if len(command) < 4:
                        raise InvalidCommandException(
                            "Invalid SUBMIT_BID command. The syntax is: SUBMIT_BID <member_id> <event_id> <b1> <b2> <b3>..."
                        )

                    member_id = command[1]
                    event_id = command[2]

                    try:
                        bids = list(map(int, command[3:]))
                    except ValueError:
                        raise InvalidCommandException(
                            "Invalid bids value. Bids should be space separated integers"
                        )

                    system.submit_bid(member_id, event_id, bids)

                elif command[0] == "DECLARE_WINNER":
                    if len(command) != 2:
                        raise InvalidCommandException(
                            "Invalid DECLARE_WINNER command. The syntax is: DECLARE_WINNER <event_id>"
                        )

                    event_id = command[1]
                    system.declare_winner(event_id)

                elif command[0] == "LIST_WINNERS":
                    if len(command) != 2:
                        raise InvalidCommandException(
                            "Invalid LIST_WINNERS command. The syntax is: LIST_WINNERS <order_by>"
                        )

                    order_by = command[1]
                    system.list_winners(order_by)

                elif command[0] == "EXIT":
                    break

                else:
                    raise InvalidCommandException("Invalid command")

            except Exception as bidding_cli_exception:
                print(bidding_cli_exception)


if __name__ == "__main__":
    BiddingCli.run()

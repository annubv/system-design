from entities.ticket import Ticket
from enums.payment_type import PaymentType


class Billing:
    @staticmethod
    def process_payment(ticket: Ticket, payment_type: PaymentType):
        if payment_type == PaymentType.ONLINE:
            # can have a pg gateway service/adapter integrated here
            print(
                f"Processed online payment of ticket {ticket.ticket_id}, amount Rs.{ticket.amount}"
            )
        else:
            print(
                f"Processed offline payment of ticket {ticket.ticket_id}, amount Rs.{ticket.amount}"
            )
        ticket.mark_as_paid()
        # we will store billing details, lets keep it simple for now
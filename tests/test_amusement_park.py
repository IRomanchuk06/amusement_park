import unittest
from unittest.mock import patch
from src.models.park_models import Attraction, Queue, CashRegister
from src.models.amusement_park import AmusementPark
from src.models.visitor import Visitor


class TestAmusementPark(unittest.TestCase):

    def setUp(self):
        self.park = AmusementPark()
        self.cash_register = CashRegister(100.0)
        self.park.cash_register = self.cash_register

        self.attraction_1 = Attraction("Roller Coaster", 12, 1.5, 5, 2, 10.0)
        self.attraction_2 = Attraction("Ferris Wheel", 5, 1.2, 5, 2, 8.0)

        self.park.add_attraction(self.attraction_1)
        self.park.add_attraction(self.attraction_2)

        self.visitor_1 = Visitor("John", 20, 1.75, 50.0)
        self.visitor_2 = Visitor("Jane", 22, 1.60, 60.0)

        self.park.visitors.append(self.visitor_1)
        self.park.visitors.append(self.visitor_2)

        self.queue_1 = Queue(self.attraction_1)
        self.queue_2 = Queue(self.attraction_2)

        self.queue_1.add_to_queue(self.visitor_1)
        self.queue_2.add_to_queue(self.visitor_2)

        self.park.queues.append(self.queue_1)
        self.park.queues.append(self.queue_2)

    def test_show_park_status(self):
        with patch('builtins.print') as mock_print:
            self.park.show_park_status()

            mock_print.assert_any_call("\nCurrent status of the park:")
            mock_print.assert_any_call(f"\n{self.attraction_1.name} - OPEN:")
            mock_print.assert_any_call(
                f"  Min Age: {self.attraction_1.min_age} | Min Height: {self.attraction_1.min_height}m | Price: ${self.attraction_1.ticket_price:.2f}")
            mock_print.assert_any_call(
                f"  {self.attraction_1.sold_tickets}/{self.attraction_1.ticket_limit} tickets sold.")

            mock_print.assert_any_call(f"\nQueue for {self.attraction_1.name}:")
            mock_print.assert_any_call(f"  Total in queue: {len(self.queue_1.queue)} people.")
            mock_print.assert_any_call(f"  1. {self.visitor_1.name} (Balance: ${self.visitor_1.balance:.2f})")

            mock_print.assert_any_call(f"\nPark balance: {self.park.cash_register.get_balance()} units.")

            mock_print.assert_any_call("\nVisitors currently in the park:")
            mock_print.assert_any_call(
                f"  {self.visitor_1.name} - Age: {self.visitor_1.age}, Height: {self.visitor_1.height}m, Balance: ${self.visitor_1.balance:.2f}")
            mock_print.assert_any_call(
                f"  Tickets: {len([ticket for ticket in self.visitor_1.tickets if not ticket.used])} valid tickets.")


if __name__ == '__main__':
    unittest.main()

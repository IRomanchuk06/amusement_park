import unittest
from unittest.mock import patch

from src.models.park_models import Attraction, Queue, CashRegister
from src.models.amusement_park import AmusementPark
from src.models.visitor import Visitor
from src.models.workers import Cashier, RideManager


class TestAmusementPark(unittest.TestCase):

    def setUp(self):
        self.park = AmusementPark()
        self.visitor = Visitor("John", 20, 1.75, 50.0)
        self.attraction = Attraction("Roller Coaster", 12, 1.5, 5, 2, 10.0)
        self.park.add_attraction(self.attraction)
        self.cash_register = CashRegister(0.0)
        self.cashier = Cashier("Mary", self.cash_register)
        self.queue = Queue(self.attraction)
        self.ride_manager = RideManager("Alice")

    def test_manage_queue_and_start(self):
        self.cashier.sell_ticket(self.visitor, self.attraction)
        self.queue.add_to_queue(self.visitor)

        self.assertFalse(self.attraction.is_running)
        self.ride_manager.manage_queue_and_start(self.attraction, self.queue)

        self.assertTrue(self.visitor.tickets[0].used)
        self.assertEqual(self.attraction.sold_tickets_stat, 1)
        self.assertTrue(self.queue.is_queue_empty())

    def test_no_valid_ticket_for_visitor(self):
        visitor_without_ticket = Visitor("Jane", 20, 1.75, 50.0)
        self.queue.add_to_queue(visitor_without_ticket)

        self.assertFalse(self.attraction.is_running)
        self.ride_manager.manage_queue_and_start(self.attraction, self.queue)

        self.assertFalse(self.attraction.is_running)
        self.assertTrue(self.queue.is_queue_empty())

    def test_add_attraction(self):
        self.assertEqual(len(self.park.attractions), 1)
        self.assertEqual(self.park.attractions[0].name, "Roller Coaster")

    def test_add_visitor(self):
        self.park.add_visitor(self.visitor)
        self.assertEqual(len(self.park.visitors), 1)
        self.assertEqual(self.park.visitors[0].name, "John")

    def test_cashier_sell_ticket(self):
        self.cashier.sell_ticket(self.visitor, self.attraction)
        self.assertEqual(len(self.visitor.tickets), 1)
        self.assertEqual(self.visitor.balance, 40.0)

    def test_no_ticket_for_visitor(self):
        visitor = Visitor("Jane", 15, 1.6, 5.0)
        self.cashier.sell_ticket(visitor, self.attraction)
        self.assertEqual(len(visitor.tickets), 0)

    def test_earn_money_for_visitor(self):
        self.visitor.earn_money(20.0)
        self.assertEqual(self.visitor.balance, 70.0)

    def test_ticket_usage(self):
        self.cashier.sell_ticket(self.visitor, self.attraction)
        ticket = self.visitor.tickets[0]
        self.assertFalse(ticket.used)
        self.visitor.use_ticket(self.attraction)
        self.assertTrue(ticket.used)


if __name__ == "__main__":
    unittest.main()

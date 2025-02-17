from workers import *


class AmusementPark:
    def __init__(self):
        self.attractions = []
        self.visitors = []
        self.queues = []
        self.cash_register = CashRegister(0.0)
        self.ride_controllers = []

    def add_attraction(self, attraction: Attraction):
        self.attractions.append(attraction)
        self.queues.append(Queue(attraction))
        print(f"Attraction {attraction.name} added to the park.")

    def add_visitor(self, visitor: Visitor):
        self.visitors.append(visitor)
        print(f"Visitor {visitor.name} has entered the park.")

    def add_cashier(self, cashier: Cashier):
        self.ride_controllers.append(cashier)
        print(f"Cashier {cashier.name} is working in the park.")

    def show_park_status(self):
        print("\nCurrent status of the park:")
        for attraction in self.attractions:
            print(f"{attraction.name}: {attraction.sold_tickets}/{attraction.ticket_limit} tickets sold.")
        for queue in self.queues:
            print(f"Queue for {queue.attraction.name}: {len(queue.queue)} people.")
        print(f"Park balance: {self.cash_register.get_money()} units.")
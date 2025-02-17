from src.models.workers import *
from src.serialization import save_to_file, load_from_file

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
            status = "OPEN" if attraction.has_available_tickets() else "SOLD OUT"
            print(f"\n{attraction.name} - {status}:")
            print(
                f"  Min Age: {attraction.min_age} | Min Height: {attraction.min_height}m | Price: ${attraction.ticket_price:.2f}")
            print(f"  {attraction.sold_tickets}/{attraction.ticket_limit} tickets sold.")
            print(f"  Tickets available: {attraction.ticket_limit - attraction.sold_tickets}")

        for queue in self.queues:
            attraction = queue.attraction
            print(f"\nQueue for {attraction.name}:")
            print(f"  Total in queue: {len(queue.queue)} people.")
            for i, visitor in enumerate(queue.queue, 1):
                print(f"  {i}. {visitor.name} (Balance: ${visitor.balance:.2f})")

        print(f"\nPark balance: {self.cash_register.get_balance()} units.")

        if self.visitors:
            print("\nVisitors currently in the park:")
            for visitor in self.visitors:
                print(
                    f"  {visitor.name} - Age: {visitor.age}, Height: {visitor.height}m, Balance: ${visitor.balance:.2f}")
                print(f"  Tickets: {len([ticket for ticket in visitor.tickets if not ticket.used])} valid tickets.")
        else:
            print("No visitors in the park.")

    def save_park_state(self, filename: str):
        save_to_file(self, filename)

    @staticmethod
    def load_park_state(filename: str):
        return load_from_file(filename)
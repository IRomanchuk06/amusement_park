import time

from src.models.visitor import Visitor

class Attraction:
    def __init__(self, name: str, min_age: int, min_height: float, ticket_limit: int, ride_duration: int,
                 ticket_price: float):
        self.name = name
        self.min_age = min_age
        self.min_height = min_height
        self.ticket_limit = ticket_limit
        self.sold_tickets = 0
        self.ride_duration = ride_duration
        self.ticket_price = ticket_price
        self.is_running = False

    def check_requirements(self, visitor):
        issues = []
        if visitor.age < self.min_age:
            issues.append("age requirement not met")
        if visitor.height < self.min_height:
            issues.append("height requirement not met")

        if issues:
            return False, f"{visitor.name} does not meet the {' and '.join(issues)} for {self.name}."

        return True, f"{visitor.name} meets all requirements for {self.name}."

    def sell_ticket(self):
        if self.sold_tickets < self.ticket_limit:
            self.sold_tickets += 1
            return Ticket(self)
        return None

    def reset(self):
        self.is_running = False
        self.sold_tickets = 0

    def start_ride(self):
        if self.is_running:
            print(f"{self.name} is already running.")
            return
        if self.sold_tickets == 0:
            print(f"No tickets sold for {self.name}. Cannot start the ride.")
            return

        self.is_running = True
        print(f"Starting the ride for {self.name} with {self.sold_tickets} passengers.")
        time.sleep(self.ride_duration)  # Simulating ride
        self.end_ride()

    def end_ride(self):
        print(f"Ride {self.name} has finished.")
        self.sold_tickets = 0
        self.is_running = False
        print(f"Tickets for {self.name} have been reset for the next ride.")

class Ticket:
    def __init__(self, attraction: Attraction):
        self.attraction = attraction
        self.price = attraction.ticket_price
        self.used = False


class Queue:
    def __init__(self, attraction: Attraction):
        self.attraction = attraction
        self.queue = []

    def add_to_queue(self, visitor: Visitor):
        if visitor in self.queue:
            print(f"{visitor.name} is already in the queue for {self.attraction.name}.")
        else:
            self.queue.append(visitor)
            print(f"{visitor.name} has joined the queue for {self.attraction.name}.")

    def process_queue(self):
        if not self.queue:
            print(f"No one in the queue for {self.attraction.name}.")
            return None

        to_remove = []
        for visitor in self.queue:
            if any(ticket.attraction == self.attraction and not ticket.used for ticket in visitor.tickets):
                visitor.use_ticket(self.attraction)
                print(f"{visitor.name} is now enjoying the {self.attraction.name}.")
                to_remove.append(visitor)
                return visitor
            else:
                print(f"{visitor.name} does not have a valid ticket for {self.attraction.name}.")
                to_remove.append(visitor)

        for visitor in to_remove:
            self.queue.remove(visitor)

        return None

    def is_queue_empty(self):
        return len(self.queue) == 0

class CashRegister:
    def __init__(self, balance: float = 0.0):
        self.balance = balance

    def add_money(self, amount: float):
        if amount > 0:
            self.balance += amount

    def get_balance(self) -> float:
        return self.balance
import time

from src.models.workers import Cashier


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

class Visitor:
    def __init__(self, name: str, age: int, height: float, balance: float):
        self.name = name
        self.age = age
        self.height = height
        self.tickets = []
        self.balance = balance

    def buy_ticket(self, cashier: Cashier, attraction: Attraction):
        cashier.sell_ticket(self, attraction)

    def choose_attraction(self, choice: int = None):
        if not self.tickets:
            print(f"{self.name} has not bought any tickets yet.")
            return None

        if choice is None:
            print(f"\n{self.name}, choose an attraction from your tickets:")
            for idx, ticket in enumerate(self.tickets, 1):
                print(f"{idx}. {ticket.attraction.name}")
            choice = int(input("Enter the attraction number: ")) - 1

        if 0 <= choice < len(self.tickets):
            selected_ticket = self.tickets[choice]
            if selected_ticket.used:
                print(f"Ticket for {selected_ticket.attraction.name} has already been used.")
                return None
            return selected_ticket.attraction
        else:
            print("Invalid choice.")
            return None

    def earn_money(self, amount: float):
        if amount < 0:
            print("Amount to earn cannot be negative.")
            return
        self.balance += amount
        print(f"{self.name} earned {amount} units. New balance: {self.balance}.")

    def use_ticket(self, attraction):
        for ticket in self.tickets:
            if ticket.attraction == attraction and not ticket.used:
                ticket.used = True
                print(f"{self.name} used the ticket for {attraction.name}.")
                return
        print(f"{self.name} has no valid ticket for {attraction.name}.")


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
    def __init__(self, balance: float):
        self.balance = balance
        self.sold_tickets = {}

    def add_money(self, amount: float):
        self.balance += amount

    def get_money(self) -> float:
        return self.balance

from park_models import *


class Worker:
    def __init__(self, name: str):
        self.name = name


class Cashier(Worker):
    def __init__(self, name: str, cash_register: CashRegister):
        super().__init__(name)
        self.cash_register = cash_register

    def show_attractions(self, attractions: list):
        print("Available attractions:")
        for idx, attraction in enumerate(attractions, 1):
            print(f"{idx}. {attraction.name} - {attraction.ticket_price} units")

    def sell_ticket(self, visitor: Visitor, attraction: Attraction):
        if visitor.balance < attraction.ticket_price:
            print(f"{visitor.name} does not have enough money for {attraction.name}.")
            return
        valid, message = attraction.check_requirements(visitor)
        if not valid:
            print(message)
            return
        ticket = attraction.sell_ticket()
        if ticket:
            visitor.tickets.append(ticket)
            visitor.balance -= attraction.ticket_price
            self.cash_register.add_money(attraction.ticket_price)
            print(f"Ticket sold to {visitor.name} for {attraction.name}.")
        else:
            print(f"No more tickets available for {attraction.name}.")

class RideManager(Worker):
    def __init__(self, name: str):
        super().__init__(name)

    def manage_queue_and_start(self, attraction: Attraction, queue: Queue):
        while not queue.is_queue_empty():
            visitor = queue.process_queue()
            if visitor:
                visitor.use_ticket(attraction)
                attraction.start_ride()
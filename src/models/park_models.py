class Attraction:
    def __init__(self, name: str, min_age: int, min_height: float, ticket_limit: int, ride_duration: int,
                 ticket_price: float):
        self.name = name
        self.min_age = min_age
        self.min_height = min_height
        self.ticket_limit = ticket_limit
        self.sold_tickets = 0
        self.ride_duration = ride_duration
        self.is_running = False
        self.ticket_price = ticket_price


class Visitor:
    def __init__(self, name: str, age: int, height: float):
        self.name = name
        self.age = age
        self.height = height
        self.tickets = []


class Ticket:
    def __init__(self, attraction: Attraction):
        self.attraction = attraction
        self.price = attraction.ticket_price
        self.used = False


class Queue:
    def __init__(self, attraction: Attraction):
        self.attraction = attraction
        self.queue = []


class CashRegister:
    def __init__(self, balance: float):
        self.balance = balance
        self.sold_tickets = {}

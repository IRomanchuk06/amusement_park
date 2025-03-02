from src.utils.park_utils import AmusementParkUtils

class Visitor:
    def __init__(self, name: str, age: int, height: float, balance: float):
        self.name = name
        self.age = age
        self.height = height
        self.tickets = []
        self.balance = balance

    def choose_attraction(self):
        if not self.tickets:
            print(f"{self.name} has not bought any tickets yet.")
            return None

        print(f"\n{self.name}, choose an attraction from your tickets:")
        for idx, ticket in enumerate(self.tickets, 1):
            print(f"{idx}. {ticket.attraction.name}")

        choice = AmusementParkUtils.get_menu_choice("Enter the attraction number: ", range(1, len(self.tickets) + 1)) - 1

        if choice < 0 or choice >= len(self.tickets):
            print(f"Invalid choice. Please choose a number between 1 and {len(self.tickets)}.")
            return None

        selected_ticket = self.tickets[choice]
        if selected_ticket.used:
            print(f"Ticket for {selected_ticket.attraction.name} has already been used.")
            return None

        return selected_ticket.attraction

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

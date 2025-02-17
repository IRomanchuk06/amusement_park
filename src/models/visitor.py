class Visitor:
    def __init__(self, name: str, age: int, height: float, balance: float):
        self.name = name
        self.age = age
        self.height = height
        self.tickets = []
        self.balance = balance

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

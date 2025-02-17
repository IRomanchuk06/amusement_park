from src import utils
from src.models.workers import Cashier, RideManager
from src.models.park_models import Attraction, Visitor
from src.models.amusement_park import AmusementPark


class ParkInterface:
    def __init__(self):
        self.park = AmusementPark()
        self.cashier = Cashier("John", self.park.cash_register)
        self.ride_manager = RideManager("Emily")
        self._initialize_sample_data()

    def _initialize_sample_data(self):
        self.park.add_attraction(Attraction("Roller Coaster", 12, 1.4, 5, 5, 10.0))
        self.park.add_attraction(Attraction("Ferris Wheel", 5, 1.0, 10, 3, 5.0))
        self.park.add_cashier(self.cashier)

    def save_to_file(self, filename):
        try:
            self.park.save_park_state(filename)
            print(f"Park saved to {filename}.")
        except Exception as e:
            print(f"Error saving park: {e}")

    def load_from_file(self, filename):
        try:
            self.park = AmusementPark.load_park_state(filename)
            print(f"Park loaded from {filename}.")
        except Exception as e:
            print(f"Error loading park: {e}")

    def show_visitor_list(self):
        utils.display_header("registered visitors")
        for i, visitor in enumerate(self.park.visitors, 1):
            print(f"{i}. {visitor.name} | Age: {visitor.age} | "
                  f"Height: {visitor.height}m | Balance: ${visitor.balance:.2f}")

    def show_attraction_list(self, show_details=False):
        utils.display_header("available attractions")
        for i, attr in enumerate(self.park.attractions, 1):
            status = "OPEN" if attr.has_available_tickets() else "SOLD OUT"
            details = (f"Min Age: {attr.min_age} | Min Height: {attr.min_height}m | "
                       f"Price: ${attr.ticket_price:.2f} | Tickets: {attr.sold_tickets}/{attr.ticket_limit}")
            print(f"{i}. {attr.name} [{status}]")
            if show_details:
                print(f"   {details}")

    def add_visitor_flow(self):
        utils.display_header("new visitor registration")
        name = input("Enter visitor name: ").strip()

        if any(v.name.lower() == name.lower() for v in self.park.visitors):
            print(f"Error: Visitor '{name}' already exists!")
            return

        age = utils.get_valid_input("Enter age: ", int)
        height = utils.get_valid_input("Enter height (meters): ", float)
        balance = utils.get_valid_input("Enter initial balance: $", float)

        new_visitor = Visitor(name, age, height, balance)
        self.park.add_visitor(new_visitor)
        print(f"\nSuccess: {name} registered with initial balance of ${balance:.2f}")

    def purchase_ticket_flow(self):
        self.show_visitor_list()
        if not self.park.visitors:
            return

        vis_idx = utils.get_valid_input("\nSelect visitor number: ", int) - 1
        if vis_idx < 0 or vis_idx >= len(self.park.visitors):
            print("Invalid visitor selection!")
            return
        visitor = self.park.visitors[vis_idx]

        self.show_attraction_list(show_details=True)
        attr_idx = utils.get_valid_input("\nSelect attraction number: ", int) - 1
        if attr_idx < 0 or attr_idx >= len(self.park.attractions):
            print("Invalid attraction selection!")
            return
        attraction = self.park.attractions[attr_idx]

        if any(t.attraction == attraction and not t.used for t in visitor.tickets):
            print(f"Error: {visitor.name} already has a valid ticket for {attraction.name}")
            return

        self.cashier.sell_ticket(visitor, attraction)

    def queue_management_flow(self):
        self.show_attraction_list()
        attr_idx = utils.get_valid_input("\nSelect attraction number: ", int) - 1
        if attr_idx < 0 or attr_idx >= len(self.park.attractions):
            print("Invalid attraction selection!")
            return
        attraction = self.park.attractions[attr_idx]
        queue = self.park.queues[attr_idx]

        self.show_visitor_list()
        vis_idx = utils.get_valid_input("\nSelect visitor number: ", int) - 1
        if vis_idx < 0 or vis_idx >= len(self.park.visitors):
            print("Invalid visitor selection!")
            return
        visitor = self.park.visitors[vis_idx]

        if not any(t.attraction == attraction and not t.used for t in visitor.tickets):
            print(f"Error: {visitor.name} doesn't have a valid ticket for {attraction.name}")
            return

        queue.add_to_queue(visitor)
        print(f"\n{visitor.name} added to {attraction.name} queue")

    def run_attraction_flow(self):
        self.show_attraction_list()
        try:
            attr_idx = int(input("\nSelect attraction number: ")) - 1
            attraction = self.park.attractions[attr_idx]
            queue = self.park.queues[attr_idx]
        except (IndexError, ValueError):
            print("Invalid attraction selection!")
            return

        print(f"\nStarting {attraction.name} operation...")
        self.ride_manager.manage_queue_and_start(attraction, queue)
        attraction.start_ride()

    def increase_visitor_balance(self):
        self.show_visitor_list()
        if not self.park.visitors:
            print("No visitors registered yet!")
            return

        vis_idx = utils.get_valid_input("\nSelect visitor number: ", int) - 1
        if vis_idx < 0 or vis_idx >= len(self.park.visitors):
            print("Invalid visitor selection!")
            return

        visitor = self.park.visitors[vis_idx]
        amount = utils.get_valid_input(f"Enter amount to add to {visitor.name}'s balance: $", float)

        visitor.earn_money(amount)
        print(f"\nSuccess: {visitor.name}'s new balance is ${visitor.balance:.2f}")

    def add_attraction_flow(self):
        utils.display_header("new attraction registration")
        name = input("Enter attraction name: ").strip()
        min_age = utils.get_valid_input("Enter minimum age: ", int)
        min_height = utils.get_valid_input("Enter minimum height (meters): ", float)
        ticket_price = utils.get_valid_input("Enter ticket price: $", float)
        ticket_limit = utils.get_valid_input("Enter ticket limit: ", int)
        sold_tickets = utils.get_valid_input("Enter sold tickets: ", int)

        new_attraction = Attraction(name, min_age, min_height, ticket_limit, sold_tickets, ticket_price)
        self.park.add_attraction(new_attraction)
        print(f"\nSuccess: {name} added as a new attraction")

    def main_menu(self):
        while True:
            utils.display_header("amusement park management system")
            print("1. Register New Visitor")
            print("2. View Attractions")
            print("3. Purchase Ticket")
            print("4. Join Ride Queue")
            print("5. Operate Attraction")
            print("6. Park Status Overview")
            print("7. Save Park State")
            print("8. Load Park State")
            print("9. Add New Attraction")
            print("10. Top Up Visitor Balance")
            print("11. Exit System")

            choice = utils.get_menu_choice("\nEnter option number: ", range(1, 12))

            if choice == 1:
                self.add_visitor_flow()
            elif choice == 2:
                self.show_attraction_list(show_details=True)
            elif choice == 3:
                self.purchase_ticket_flow()
            elif choice == 4:
                self.queue_management_flow()
            elif choice == 5:
                self.run_attraction_flow()
            elif choice == 6:
                self.park.show_park_status()
            elif choice == 7:
                filename = input("Enter the filename to save park state: ")
                self.save_to_file(filename)
            elif choice == 8:
                filename = input("Enter the filename to load park state: ")
                self.load_from_file(filename)
            elif choice == 9:
                self.add_attraction_flow()
            elif choice == 10: 
                self.increase_visitor_balance()
            elif choice == 11:
                print("\nExiting system... Thank you for using Park Manager!")
                break
            else:
                print("Invalid selection. Please choose 1-10")

            input("\nPress Enter to continue...")

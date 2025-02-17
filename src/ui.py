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
        """Initialize sample attractions for demonstration"""
        self.park.add_attraction(Attraction("Roller Coaster", 12, 1.4, 5, 5, 10.0))
        self.park.add_attraction(Attraction("Ferris Wheel", 5, 1.0, 10, 3, 5.0))
        self.park.add_cashier(self.cashier)

    def display_header(self, title):
        """Display formatted header"""
        print(f"\n{'=' * 40}")
        print(f"{title.upper():^40}")
        print(f"{'=' * 40}")

    def get_valid_input(self, prompt, input_type=float):
        """Handle user input with validation"""
        while True:
            try:
                return input_type(input(prompt))
            except ValueError:
                print("Invalid input. Please try again.")

    def show_visitor_list(self):
        """Display formatted list of visitors"""
        self.display_header("registered visitors")
        for i, visitor in enumerate(self.park.visitors, 1):
            print(f"{i}. {visitor.name} | Age: {visitor.age} | "
                  f"Height: {visitor.height}m | Balance: ${visitor.balance:.2f}")

    def show_attraction_list(self, show_details=False):
        """Display formatted list of attractions"""
        self.display_header("available attractions")
        for i, attr in enumerate(self.park.attractions, 1):
            status = "OPEN" if attr.has_available_tickets() else "SOLD OUT"
            details = (f"Min Age: {attr.min_age} | Min Height: {attr.min_height}m | "
                       f"Price: ${attr.ticket_price:.2f} | Tickets: {attr.sold_tickets}/{attr.ticket_limit}")
            print(f"{i}. {attr.name} [{status}]")
            if show_details:
                print(f"   {details}")

    def add_visitor_flow(self):
        """Handle visitor registration process"""
        self.display_header("new visitor registration")
        name = input("Enter visitor name: ").strip()

        if any(v.name.lower() == name.lower() for v in self.park.visitors):
            print(f"Error: Visitor '{name}' already exists!")
            return

        age = self.get_valid_input("Enter age: ", int)
        height = self.get_valid_input("Enter height (meters): ", float)
        balance = self.get_valid_input("Enter initial balance: $", float)

        new_visitor = Visitor(name, age, height, balance)
        self.park.add_visitor(new_visitor)
        print(f"\nSuccess: {name} registered with initial balance of ${balance:.2f}")

    def purchase_ticket_flow(self):
        """Handle ticket purchasing process"""
        self.show_visitor_list()
        if not self.park.visitors:
            return

        try:
            vis_idx = int(input("\nSelect visitor number: ")) - 1
            visitor = self.park.visitors[vis_idx]
        except (IndexError, ValueError):
            print("Invalid visitor selection!")
            return

        self.show_attraction_list(show_details=True)
        try:
            attr_idx = int(input("\nSelect attraction number: ")) - 1
            attraction = self.park.attractions[attr_idx]
        except (IndexError, ValueError):
            print("Invalid attraction selection!")
            return

        # Check existing valid tickets
        if any(t.attraction == attraction and not t.used for t in visitor.tickets):
            print(f"Error: {visitor.name} already has a valid ticket for {attraction.name}")
            return

        # Process ticket purchase
        self.cashier.sell_ticket(visitor, attraction)

    def queue_management_flow(self):
        """Handle queue management process"""
        self.show_attraction_list()
        try:
            attr_idx = int(input("\nSelect attraction number: ")) - 1
            attraction = self.park.attractions[attr_idx]
            queue = self.park.queues[attr_idx]
        except (IndexError, ValueError):
            print("Invalid attraction selection!")
            return

        self.show_visitor_list()
        try:
            vis_idx = int(input("\nSelect visitor number: ")) - 1
            visitor = self.park.visitors[vis_idx]
        except (IndexError, ValueError):
            print("Invalid visitor selection!")
            return

        # Check for valid ticket
        if not any(t.attraction == attraction and not t.used for t in visitor.tickets):
            print(f"Error: {visitor.name} doesn't have a valid ticket for {attraction.name}")
            return

        queue.add_to_queue(visitor)
        print(f"\n{visitor.name} added to {attraction.name} queue")

    def run_attraction_flow(self):
        """Handle attraction operation process"""
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

    def main_menu(self):
        """Display and manage main menu interface"""
        while True:
            self.display_header("amusement park management system")
            print("1. Register New Visitor")
            print("2. View Attractions")
            print("3. Purchase Ticket")
            print("4. Join Ride Queue")
            print("5. Operate Attraction")
            print("6. Park Status Overview")
            print("7. Exit System")

            choice = input("\nEnter option number: ").strip()

            if choice == "1":
                self.add_visitor_flow()
            elif choice == "2":
                self.show_attraction_list(show_details=True)
            elif choice == "3":
                self.purchase_ticket_flow()
            elif choice == "4":
                self.queue_management_flow()
            elif choice == "5":
                self.run_attraction_flow()
            elif choice == "6":
                self.park.show_park_status()
            elif choice == "7":
                print("\nExiting system... Thank you for using Park Manager!")
                break
            else:
                print("Invalid selection. Please choose 1-7")

            input("\nPress Enter to continue...")

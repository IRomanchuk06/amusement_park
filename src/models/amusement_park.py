from park_models import CashRegister


class AmusementPark:
    def __init__(self):
        self.attractions = []
        self.visitors = []
        self.queues = []
        self.cash_register = CashRegister(0.0)
        self.ride_controllers = []

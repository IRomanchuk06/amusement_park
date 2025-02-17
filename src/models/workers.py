from park_models import CashRegister


class Worker:
    def __init__(self, name: str):
        self.name = name


class Cashier(Worker):
    def __init__(self, name: str, cash_register: CashRegister):
        super().__init__(name)
        self.cash_register = cash_register


class RideManager(Worker):
    def __init__(self, name: str):
        super().__init__(name)

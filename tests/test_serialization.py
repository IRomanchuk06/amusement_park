import unittest
import os
from src.models.park_models import Visitor, Attraction
from src.models.amusement_park import AmusementPark
from src.models.workers import Cashier


class TestSerialization(unittest.TestCase):

    def setUp(self):
        self.park = AmusementPark()
        self.cashier = Cashier("John", self.park.cash_register)
        self.park.add_cashier(self.cashier)
        self.visitor = Visitor("Alice", 25, 1.75, 50.0)
        self.park.add_visitor(self.visitor)
        self.attraction = Attraction("Roller Coaster", 12, 1.4, 5, 5, 10.0)
        self.park.add_attraction(self.attraction)

    def test_save_load_park(self):
        filename = 'test_park_state.pkl'

        try:
            self.park.save_park_state(filename)
        except Exception as e:
            self.fail(f"Error during save: {e}")

        loaded_park = None
        try:
            loaded_park = AmusementPark.load_park_state(filename)
        except Exception as e:
            self.fail(f"Error during load: {e}")

        self.assertIsInstance(loaded_park, AmusementPark)
        self.assertEqual(len(loaded_park.visitors), 1)
        self.assertEqual(loaded_park.visitors[0].name, self.visitor.name)
        self.assertEqual(len(loaded_park.attractions), 1)
        self.assertEqual(loaded_park.attractions[0].name, self.attraction.name)
        self.assertEqual(len(loaded_park.ride_controllers), 1)
        self.assertEqual(loaded_park.ride_controllers[0].name, self.cashier.name)

        if os.path.exists(filename):
            os.remove(filename)

    def test_save_load_empty_park(self):
        empty_park = AmusementPark()
        filename = 'test_empty_park.pkl'

        try:
            empty_park.save_park_state(filename)
        except Exception as e:
            self.fail(f"Error during save: {e}")

        loaded_empty_park = None
        try:
            loaded_empty_park = AmusementPark.load_park_state(filename)
        except Exception as e:
            self.fail(f"Error during load: {e}")

        self.assertIsInstance(loaded_empty_park, AmusementPark)
        self.assertEqual(len(loaded_empty_park.visitors), 0)
        self.assertEqual(len(loaded_empty_park.attractions), 0)
        self.assertEqual(len(loaded_empty_park.ride_controllers), 0)

        if os.path.exists(filename):
            os.remove(filename)

    def test_load_invalid_file(self):
        invalid_filename = 'invalid_park_state.pkl'

        loaded_park = None
        try:
            loaded_park = AmusementPark.load_park_state(invalid_filename)
        except Exception as e:
            self.assertIsNone(loaded_park)
            print(f"Error loading file: {e}")

        if os.path.exists(invalid_filename):
            os.remove(invalid_filename)

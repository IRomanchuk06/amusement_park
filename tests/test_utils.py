import unittest
from unittest.mock import patch
from io import StringIO

from src.utils import *


class TestUserInputFunctions(unittest.TestCase):

    @patch('builtins.input', return_value='2')
    def test_get_menu_choice_valid(self, mock_input):
        valid_choices = range(1, 5)
        result = get_menu_choice("Choose a number between 1 and 4: ", valid_choices)
        self.assertEqual(result, 2)

    @patch('builtins.input', side_effect=['6', '3'])
    @patch('builtins.print')
    def test_get_menu_choice_invalid(self, mock_print, mock_input):
        valid_choices = range(1, 5)
        result = get_menu_choice("Choose a number between 1 and 4: ", valid_choices)
        self.assertEqual(result, 3)
        mock_print.assert_called_with("Invalid choice. Please choose a number between 1 and 4.")

    @patch('builtins.input', side_effect=['abc', '3'])
    @patch('builtins.print')
    def test_get_menu_choice_invalid_input_type(self, mock_print, mock_input):
        valid_choices = range(1, 5)
        result = get_menu_choice("Choose a number between 1 and 4: ", valid_choices)
        self.assertEqual(result, 3)
        mock_print.assert_called_with("Invalid input. Please enter a valid number.")

    @patch('builtins.input', return_value='3.14')
    def test_get_valid_input_float(self, mock_input):
        result = get_valid_input("Enter a valid float: ", float)
        self.assertEqual(result, 3.14)

    @patch('builtins.input', side_effect=['abc', '3.14'])
    @patch('builtins.print')
    def test_get_valid_input_invalid_float(self, mock_print, mock_input):
        result = get_valid_input("Enter a valid float: ", float)
        self.assertEqual(result, 3.14)
        mock_print.assert_called_with("Invalid input. Please try again.")

    @patch('builtins.input', return_value='123')
    def test_get_valid_input_int(self, mock_input):
        result = get_valid_input("Enter a valid integer: ", int)
        self.assertEqual(result, 123)

    @patch('builtins.input', side_effect=['abc', '456'])
    @patch('builtins.print')
    def test_get_valid_input_invalid_int(self, mock_print, mock_input):
        result = get_valid_input("Enter a valid integer: ", int)
        self.assertEqual(result, 456)
        mock_print.assert_called_with("Invalid input. Please try again.")

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_header(self, mock_stdout):
        display_header("Test Title")
        output = mock_stdout.getvalue().strip()
        expected_output = "========================================\n               TEST TITLE               \n========================================"
        self.assertEqual(output, expected_output)

if __name__ == '__main__':
    unittest.main()
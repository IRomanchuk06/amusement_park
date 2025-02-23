class AmusementParkUtils:
    def __init__(self):
        pass

    @staticmethod
    def get_menu_choice(prompt: str, valid_choices: range) -> int:
        while True:
            try:
                choice = int(input(prompt))
                if choice in valid_choices:
                    return choice
                else:
                    print(f"Invalid choice. Please choose a number between {valid_choices.start} and {valid_choices.stop - 1}.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    @staticmethod
    def get_valid_input(prompt, input_type=float, condition=lambda x: True, error_message="Invalid input. Please try again."):
        while True:
            try:
                value = input_type(input(prompt))
                if condition(value):
                    return value
                else:
                    print(error_message)
            except ValueError:
                print(error_message)

    @staticmethod
    def get_age(prompt):
        return AmusementParkUtils.get_valid_input(prompt, int, lambda x: 0 <= x <= 120, "Age must be between 0 and 120.")

    @staticmethod
    def get_num_greater_0(prompt):
        return AmusementParkUtils.get_valid_input(prompt, float, lambda x: x > 0, "Number must be greater than 0.")

    @staticmethod
    def get_height(prompt):
        return AmusementParkUtils.get_valid_input(prompt, float, lambda x: 0 <= x <= 300, "Height must be between 0 and 300.")

    @staticmethod
    def display_header(title):
        print(f"\n{'=' * 40}")
        print(f"{title.upper():^40}")
        print(f"{'=' * 40}")

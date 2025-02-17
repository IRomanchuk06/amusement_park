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

def get_valid_input(prompt, input_type=float):
    while True:
        try:
            return input_type(input(prompt))
        except ValueError:
            print("Invalid input. Please try again.")
        
def display_header(title):
    print(f"\n{'=' * 40}")
    print(f"{title.upper():^40}")
    print(f"{'=' * 40}")
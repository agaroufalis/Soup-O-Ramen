def get_valid_input(prompt, valid_options):

    while True:

        choice = input(prompt).strip()

        # Normalize letter inputs
        if choice.isalpha():
            choice = choice.title()

        if choice in valid_options:
            return choice

        print(
            f"Invalid choice. "
            f"Options: {', '.join(valid_options)}"
        )


def get_non_empty_input(prompt):

    while True:

        value = input(prompt).strip()

        if value:
            return value

        print("Input cannot be blank.")


def get_positive_int(prompt):

    while True:

        try:

            value = int(input(prompt))

            if value > 0:
                return value

            print("Must be greater than 0.")

        except ValueError:
            print("Enter a valid number.")
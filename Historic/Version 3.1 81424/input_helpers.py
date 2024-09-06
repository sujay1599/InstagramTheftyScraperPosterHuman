def get_input(prompt, input_type=str, retries=3):
    while retries > 0:
        try:
            return input_type(input(prompt))
        except ValueError:
            print(f"Invalid input. Please enter a valid {input_type.__name__}.")
            retries -= 1
    raise ValueError("Too many invalid attempts.")

def get_boolean_input(prompt):
    return input(prompt).strip().lower() in ['true', 'yes', 'y']

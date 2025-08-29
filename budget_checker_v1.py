def get_budget(min_amt=2, max_amt=50):
    while True:
        try:
            budget = float(input(f"Enter your budget ({min_amt}-{max_amt}): "))
            if min_amt < budget < max_amt:
                return budget
            print(f"Please enter a number between {min_amt} and {max_amt}")
        except ValueError:
            print("That’s not a number, try again.")

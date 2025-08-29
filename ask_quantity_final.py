def ask_quantity(item_name):
    while True:
        qty = input(f"How many {item_name} would you like? (0 to cancel) ")
        try:
            qty = int(qty)
            if qty == 0:
                return 0
            if qty > 0:
                return qty
            print("Please enter a number greater than 0.")
        except ValueError:
            print("That’s not a number.")

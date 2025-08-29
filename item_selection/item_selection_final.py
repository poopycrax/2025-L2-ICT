def item_selection(num_items):
    while True:
        try:
            ans = int(input("Enter item number (0 to quit): "))
            if 1 <= ans <= num_items:
                return ans
            if ans == 0:
                return 0
            print(f"Pick a number from 1-{num_items}.")
        except ValueError:
            print("That’s not a valid number.")

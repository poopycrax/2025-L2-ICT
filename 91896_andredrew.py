import pandas
import numpy

#heading format with decoration
def make_statement(statement, decoration):
    return f"{decoration * 3} {statement} {decoration * 3}"

#checks for yes or no input also accepts y or n, loops until valid input is given
def string_check(question, valid_answers=('yes', 'no'),
                 num_letters=1):
    while True:
        response = input(question).lower()

        for item in valid_answers:
            if response == item:
                return item
            elif response == item[:num_letters]:
                return item

        print(f"Please choose an option from {valid_answers}\n")

#prints instructions if user wants them
def instructions():
    make_statement("Instructions", "🆔")
    print('''
This program lets you shop at Apu's Dairy.

- Enter your budget.
- You will see a list of items with prices and stock.
- Pick an item by typing its number.
- Enter how many you want (if you can afford it).
- Keep shopping until you run out of money or say no.

You will get a receipt at the end.
''')

#ask for budget, ensures budget is between min and max amount. Loops until valid input is given
def get_budget(min_amt=2, max_amt=50):
    while True:
        try:
            budget = float(input(f"Enter your budget (${min_amt}-${max_amt}): $"))
            if min_amt <= budget <= max_amt:
                return budget
            print(f"Please enter a number between {min_amt} and {max_amt}")
        except ValueError:
            print("That’s not a number, try again.")

#checks if user input is blank, loops until valid input is given.
def not_blank(question):
    while True:
        response = input(question)
        if response != "":
            return response
        print("Sorry this can't be blank. Please try again. \n")

#asks user to enter there desired item from list of available items depending on budget. Loops until valid input is given.
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


#asks user how many of that item they want, allows user to cancel choice and return to item_selection with 0 input
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

def currency(x):
    return "${:.2f}".format(x)

#product name, prices and stock amount
products = ["Chocolate", "Chips", "Coke", "Lolly Bag", "Milkshake"]
prices = [3.50, 2.50, 3.00, 2.00, 5.00]
stock = [10, 15, 12, 8, 5]

#panda dataframe to display products, prices and stock amounts to user.
dairy_frame = pandas.DataFrame({
    'Product': products,
    'Price': prices,
    'Stock': stock
})
dairy_frame.index = numpy.arange(1, len(dairy_frame) + 1)

#main program
print(make_statement("Apu's Dairy", "🍫"))

#welcome message and gets users name
name = not_blank("Welcome to Apu's Dairy, What's your name? ")
#shows instructions if wanted
if string_check(f"Hello {name} you want to see the instructions? ") == "yes":
    instructions()

print()
print(dairy_frame)
print()


budget = get_budget()
cart = []
purchase_made = False

while True:
    # Filter items that are in stock AND user can afford at least 1 unit
    affordable_items = dairy_frame[(dairy_frame["Stock"] > 0)]


    #exits code if user cannot afford anything else
    if affordable_items.empty:
        print("\nYou don't have enough money to buy anything else.")
        break


    print("\nItems you can afford:")
    print(affordable_items)
    print(f"\nYou have ${budget:.2f} left.")


    # Let user choose from filtered list
    item_num = item_selection(len(affordable_items))
    if item_num == 0:  #user to chose checkout
        break
    item_name = affordable_items.loc[item_num, "Product"]
    item_price = affordable_items.loc[item_num, "Price"]
    item_stock = affordable_items.loc[item_num, "Stock"]

    quantity = ask_quantity(item_name)
    if quantity == 0:
        print("Cancelled selection.")
        continue

    max_can_buy_stock = item_stock
    max_can_buy_budget = budget // item_price
    max_can_buy = int(min(max_can_buy_stock, max_can_buy_budget))

    if quantity > max_can_buy:
        print(f"You can only buy {max_can_buy} {item_name}(s).")
        buy_max = string_check(f"Do you want to buy {max_can_buy} {item_name}(s) instead? ")
        if buy_max == "yes":
            quantity = max_can_buy
        else:
            continue


    total_cost = item_price * quantity

    if total_cost > budget:
        print("You cannot afford that many.")
        max_amount = string_check(f"Do you want to buy {item_stock} {item_name} instead? ")
        continue

    # Update budget and stock
    budget -= total_cost
    dairy_frame.loc[dairy_frame["Product"] == item_name, "Stock"] -= quantity

    # Add to cart
    cart.append({"Product": item_name, "Quantity": quantity, "Total": total_cost})

    print(f"Added {quantity} {item_name}(s) to your cart.")

    can_afford = any(stock[i] > 0 and prices[i] <= budget for i in range(len(prices)))
    if not can_afford:
        print("\nYou don't have enough money to buy anything else.")
        break

    if string_check("Do you want to buy another item? ") == "no":
        break

if not cart:   #nothing was bought
    print("You haven't bought anything. Thanks for visiting Apu's Dairy!")
else: #prints receipt
        receipt = pandas.DataFrame(cart)

        for column in ["Total"]:
            receipt[column] = receipt[column].apply(currency)

        receipt_string = receipt.to_string(index=False)

        heading_string = make_statement("Apu's Dairy Receipt", "=")
        summary_heading = make_statement("Summary", "-")

        total_cost = sum(item["Total"] for item in cart)
        summary = [f"Total Cost: {currency(total_cost)}",
                   f"Remaining Money: {currency(budget)}"
                   ]


        to_write = [heading_string, "\n",
                    name + "'s Receipt", "\n",
                    summary_heading,
                    receipt_string, "\n",
                    *summary]

        print()
        for item in to_write:
            print(item)

        file_name = "apus_dairy_receipt.txt"
        with open(file_name, "w+") as text_file:
            for item in to_write:
                text_file.write(str(item))
                text_file.write("\n")


        text_file.close()

        print(f"Thanks {name} for shopping with Apu's Dairy!")
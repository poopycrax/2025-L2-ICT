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

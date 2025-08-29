def not_blank(question):
    while True:
        response = input(question)
        if response != "":
            return response
        print("Sorry this can't be blank. Please try again. \n")
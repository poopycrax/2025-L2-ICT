# Function
def make_statement(statement, decoration, lines):
    middle = f"{decoration * 3} {statement} {decoration * 3}"
    top_bottom = decoration * len(middle)

    if lines == 1:
        print(middle)
    elif lines == 2:
        print(middle)
        print(top_bottom)

    else:
        print(top_bottom)
        print(middle)
        print(top_bottom)


# Main Routine
make_statement("Programming is Fun!", "=", 3)
print()
make_statement("Programming is Still Fun!", "*", 2)
print()
make_statement("Emoji in Action", "👍", 1)

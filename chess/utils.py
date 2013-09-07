from chess import consts

def get_coord_tuple(input_val):
    """
    We use this method to allow dynamic inputs to functions that take a coords argument.  We want to allow
    a machine friendly integer tuple and also a human friendly algebraic chess position (i.e. h6)
    """

    # Strings and tuples both take index syntax, so this works for either
    column = input_val[0]
    row = input_val[1]

    # Check type on column.  If it isn't an int, than we probably had a string chess position input like h6.
    # Use the LETTER_AND_INT_MAP to transform it into the correct integer
    if type(column) != int:
        column = consts.LETTER_AND_INT_MAP[column]

    # The row will be the right value, but it might be a string instead of an int if we took a string chess position
    # input.  So just call int on it
    row = int(row)

    # Return a machine friendly int tuple
    return (column, row)


def increment(i):
    return i + 1


def decrement(i):
    return i - 1
import re

input_string = input("adj meg egy SQL lekérdezést\n").strip()
input_string_array = input_string.split()
tables = ["A", "B", "C"]
attributes = ["a1", "a2", "b1", "b2", "c1", "c2"]
bins = 10


def check():
    words_array = []
    for word in input_string_array:
        words_array.append(word.upper())

    if (words_array[0] == "SELECT"
            and words_array[1] == "*"
            and words_array[2] == "FROM"
            and "WHERE" in words_array):
        return True
    else:
        return False


def cursor():
    table_parts = []
    where_parts = []

    mode = ("")
    for word in input_string_array:
        if word.upper() == "FROM":
            mode = "FROM"
            continue
        elif (word.upper() == "WHERE"):
            mode = "WHERE"
            continue
        if mode == "FROM":
            table_parts.append(word)
        elif mode == "WHERE":
            where_parts.append(word)

    return table_parts, where_parts


def wich_table(table_parts):
    string = "".join(table_parts).upper()
    table_bits = []
    for table in tables:
        if table in string:
            table_bits.append(1)
        else:
            table_bits.append(0)
    return table_bits


def restriction(where_parts):
    restriction_bits = []
    where = "".join(where_parts)  # Gemini
    where = re.split(r'(<=|>=|==|<|>)', where)  # Gemini
    for attribute in attributes:
        if attribute in where[0]:
            number = round(float(where[2]) / 100, 1)
            if where[1] == "<=" or where[1] == "<":
                restriction_bits.append(number)
            elif where[1] == ">=" or where[1] == ">":
                restriction_bits.append(1 - number)
            elif where[1] == "==":
                restriction_bits.append(round(1 / bins, 2))
        elif attribute[0] == where[0][0]:
            restriction_bits.append(1)
        else:
            restriction_bits.append(0)

    return restriction_bits


# SELECT * FROM A WHERE a1    <=       23

if (check()):
    whole_table = wich_table() + restriction()
    print(whole_table)

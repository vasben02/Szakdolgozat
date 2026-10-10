import re

input_string = input("adj meg egy SQL lekérdezést\n").strip()
input_string_array = input_string.split()
tables = ["A", "B", "C"]
attributes = ["a1", "a2", "b1", "b2", "c1", "c2"]
bins = 10

table_parts = []
restriction_parts = []
join_parts = []


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
    mode = ("")
    for word in input_string_array:
        if word.upper() == "FROM" or word.upper() == "JOIN":
            mode = "TABLES"
            continue
        elif word.upper() == "ON":
            mode = "JOIN"
            continue
        elif word.upper() == "WHERE":
            mode = "WHERE"
            continue

        if mode == "TABLES":
            table_parts.append(word)
        elif mode == "JOIN":
            join_parts.append(word)
        elif mode == "WHERE":
            restriction_parts.append(word)


def wich_table():
    string = "".join(table_parts).upper()
    table_bits = []
    for table in tables:
        if table in string:
            table_bits.append(1)
        else:
            table_bits.append(0)
    return table_bits


def restriction():
    restriction_bits = []
    where = "".join(restriction_parts)  # Gemini
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


def join():
    join_bits = [0, 0]
    join_str = "".join(join_parts).upper()

    if "A." in join_str and "B." in join_str:
        join_bits[0] = 1
    if "B." in join_str and "C." in join_str:
        join_bits[1] = 1

    return join_bits


if (check()):
    cursor()
    whole_table = wich_table() + restriction() + join()
    print(whole_table)

# SELECT * FROM A WHERE a1    <=       23
# SELECT * FROM A JOIN B ON A.id = B.id WHERE a1 <= 23
# SELECT * FROM A JOIN B ON A.id = B.id WHERE a1 <= 50
# SELECT * FROM B JOIN C ON B.id = C.id WHERE c1 == 25
# SELECT * FROM A WHERE a2 >= 80
# SELECT * FROM A JOIN B JOIN C ON A.id = B.id AND B.id = C.id WHERE b1 < 10

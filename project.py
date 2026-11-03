import binascii
import re
import sqlite3

original_input_string = input("adj meg egy SQL lekérdezést\n").strip()
input_string = original_input_string
alias_map = {
    "price": "a1",
    "size": "a2",
    "location_str": "b1",
    "district": "b2",
    "heating_type": "c1",
    "condition": "c2"
}

for real_name, key in alias_map.items():
    input_string = input_string.replace(real_name, key)
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
            value =  where[2].replace("'", "").replace('"', '')

            number = hashing(value)

            if where[1] == "<=" or where[1] == "<":
                restriction_bits.append(number)
            elif where[1] == ">=" or where[1] == ">":
                restriction_bits.append(round(1 - number,1))
            elif where[1] == "==":
                binning = round(number * bins) / bins
                restriction_bits.append(binning)
        elif attribute[0] == where[0][0]:
            restriction_bits.append(1)
        else:
            restriction_bits.append(0)

    return restriction_bits

def hashing(inputval):
    hash_val = binascii.crc32(inputval.encode('utf-8'))
    return round(hash_val / 0xffffffff, 1)

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
    conn = sqlite3.connect("property_database.db")
    db_cursor = conn.cursor()
    count_query = original_input_string.replace("SELECT *", "SELECT COUNT(*)")
    print(count_query)
    db_cursor.execute(count_query)
    real_count = db_cursor.fetchone()[0]
    print("Tényleges sorszám:", real_count)


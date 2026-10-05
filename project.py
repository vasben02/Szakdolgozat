import re


input_string = input("adj meg egy SQL lekérdezést\n").strip()
input_string_array = input_string.split()
tables = ["A", "B", "C"]
attributes = ["a1", "a2", "b1", "b2", "c1", "c2"]
bins = 10


def check():
    if len(input_string_array) >= 6:
        if (input_string_array[0].upper() == "SELECT" and
                input_string_array[1].upper() == "*" and
                input_string_array[2].upper() == "FROM" and
                input_string_array[4].upper() == "WHERE"):
            return True
    return False


def wich_table():
    table_bits = []
    for table in tables:
        if table == input_string_array[3].upper():
            table_bits.append(1)

        else:
            table_bits.append(0)
    return table_bits

def restriction():
    restriction_bits = []
    where = input_string_array[5:] #Gemini
    where = "".join(where) #Gemini
    where = re.split(r'(<=|>=|==|<|>)', where) #Gemini
    for attribute in attributes:
        if attribute in where[0]:
            number = round(float(where[2]) / 100, 1)
            if where[1] == "<=" or where[1] == "<":
                restriction_bits.append(number)
            elif where[1] == ">=" or where[1] == ">":
                restriction_bits.append(1 - number)
            elif where[1] == "==":
                restriction_bits.append(round(1 / bins, 2))
        elif attribute[0]==where[0][0] :
            restriction_bits.append(1)
        else:
            restriction_bits.append(0)

    return restriction_bits


# SELECT * FROM A WHERE a1    <=       23

if(check()):
    whole_table = wich_table()+restriction()
    print(whole_table)

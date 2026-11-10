import sqlite3
import random

conn = sqlite3.connect('property_database.db')
db_cursor = conn.cursor()

db_cursor.execute("SELECT MIN(price), MAX(price) FROM A")
min_price, max_price = db_cursor.fetchone()
min_price, max_price = int(min_price), int(max_price)

db_cursor.execute("SELECT MIN(size), MAX(size) FROM A")
min_size, max_size = db_cursor.fetchone()
min_size, max_size = int(min_size), int(max_size)

db_cursor.execute("SELECT DISTINCT location_str FROM B WHERE location_str IS NOT NULL")
location_str = [row[0] for row in db_cursor.fetchall()]

db_cursor.execute("SELECT DISTINCT district FROM B WHERE district IS NOT NULL")
district = [row[0] for row in db_cursor.fetchall()]

db_cursor.execute("SELECT DISTINCT heating_type FROM C WHERE heating_type IS NOT NULL")
heating_type = [row[0] for row in db_cursor.fetchall()]

db_cursor.execute("SELECT DISTINCT condition FROM C WHERE condition IS NOT NULL")
condition = [row[0] for row in db_cursor.fetchall()]

conn.close()

operators = ["<", ">", "<=", ">="]
columns = ["price", "size", "location_str", "district", "heating_type", "condition"]

with open("querys.txt", "w", encoding="utf-8") as file:
    for i in range(5000):
        chosen_column = random.choice(columns)

        if chosen_column == "price":
            chosen_operator = random.choice(operators)
            chosen_price = random.randint(min_price, max_price)
            query = f"SELECT * FROM A WHERE price {chosen_operator} {chosen_price}"

        elif chosen_column == "size":
            chosen_operator = random.choice(operators)
            chosen_size = random.randint(min_size, max_size)
            query = f"SELECT * FROM A WHERE size {chosen_operator} {chosen_size}"

        elif chosen_column == "location_str":
            chosen_location_str = random.choice(location_str)
            query = f"SELECT * FROM A JOIN B ON A.location_id = B.location_id WHERE location_str == '{chosen_location_str}'"

        elif chosen_column == "district":
            chosen_district = random.choice(district)
            query = f"SELECT * FROM A JOIN B ON A.location_id = B.location_id WHERE district == '{chosen_district}'"

        elif chosen_column == "heating_type":
            chosen_heating_type = random.choice(heating_type)
            query = f"SELECT * FROM A JOIN C ON A.property_id = C.property_id WHERE heating_type == '{chosen_heating_type}'"

        elif chosen_column == "condition":
            chosen_condition = random.choice(condition)
            query = f"SELECT * FROM A JOIN C ON A.property_id = C.property_id WHERE condition == '{chosen_condition}'"

        file.write(query + "\n")

print("success")
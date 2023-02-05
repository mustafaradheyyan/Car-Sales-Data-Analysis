import sqlite3

def open_connection():
    global conn
    conn = sqlite3.connect("database/car_sales.db")

def persist_dataset(df):
    df.to_sql("car_sales", conn, if_exists='append')

def add_data(): pass

def update_data(): pass

def read_data(): pass

def delete_data(): pass

def close_connection():
    conn.close()

# with conn:
#     conn.execute("""CREATE TABLE IF NOT EXISTS dogs (
#         dog_id INTEGER PRIMARY KEY,
#         dog_name TEXT,
#         breed TEXT
#     )""")

# with conn:
#     conn.execute("INSERT INTO dogs(dog_name, breed) VALUES ('Lunar','Labs')")

# # for row in conn.execute("SELECT * FROM dogs"):
# #     print(row)

# with conn:
#     query_result_list = [row for row in conn.execute("SELECT * FROM dogs")]
#     query_result_list = conn.execute("SELECT * FROM dogs")
#     print(query_result_list)
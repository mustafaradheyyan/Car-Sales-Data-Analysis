import sqlite3

TABLE_NAME = "car_sales"

def open_connection():
    global conn
    conn = sqlite3.connect(f"database/{TABLE_NAME}.db")

def persist_dataset(df):
    try:
        df.to_sql(TABLE_NAME, conn, if_exists='fail', index=False)
    except ValueError:
        print("Database already exists!")

def prep_qry(args, colnames):
    """this query is secure as long as `colnames` contains trusted data
    standard parametrized query mechanism secures `args`"""

    binds,use = [],[]

    for colname, value in zip(colnames,args):
        if value is not None:
            use.extend([colname,","])
            binds.extend(["?",","])


    parts = [f"insert into {TABLE_NAME} ("]
    use = use[:-1]
    binds = binds[:-1]
    
    parts.extend(use)
    parts.append(") values(")
    parts.extend(binds)
    parts.append(")")

    qry = " ".join(parts)

    return qry, tuple([v for v in args if not v is None])

def add_data(attributes):
    user_data = tuple(input(f"Enter input for {attribute}: ") for attribute in attributes)
    
    # print(prep_qry([1,None,3], attributes))
    # print(prep_qry(user_data, attributes))
    #print(str(prep_qry(user_data, attributes)))
    query, data = prep_qry(user_data, attributes)
    print(query, data)
    
    with conn:
        conn.execute(query, data)
    
    # print(user_data)
    # print(tuple(attributes))
    # query = "INSERT INTO car_sales (%s) VALUES (?)" % tuple(attributes)
    # # with conn: conn.execute(query, user_data)
    # with conn:
    #     conn.execute(query, user_data)
    #     # conn.execute("INSERT INTO car_sales (Make,Model,ColorID,VehicleType,CostPrice,SpareParts,LaborCost,Registration_Date,Mileage,PurchaseDate) VALUES (?,?,?,?,?,?,?,?,?,?)", user_data)

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
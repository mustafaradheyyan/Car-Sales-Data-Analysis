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

def add_data(attributes):
    user_data = tuple(input(f"Enter input for {attribute}: ") for attribute in attributes)
    query, data = prep_insert_qry(user_data, attributes)

    with conn:
        conn.execute(query, data)

def update_data(attributes):
    # while(True):
    #     attribute = input(f"What attribute do you want to change? ({list(attributes)})\n")
    #     if attribute not in attributes:
    #         print("That attribute is not in the table! Try again from this list:", attributes)
    #     else:
    #         break
        
    # value = input("What value do you want to set the attribute to? ")
    # conditional = input("Type in the conditional statement after the WHERE clause: ")
    
    # query = f"UPDATE {TABLE_NAME} SET MAKE = ? WHERE MAKE = ?"

    # with conn:
    #     conn.execute(query, (value, conditional))
    # conn.commit()
    
    while(True):
        attribute = input(f"What attribute do you want to change? ({list(attributes)})\n")
        if attribute not in attributes:
            print("That attribute is not in the table! Try again from this list:", attributes)
        else:
            break
        
    value = input("What value do you want to set the attribute to? ")
    conditional = input("Type in the conditional statement after the WHERE clause: ")
    
    query = f"UPDATE {TABLE_NAME} SET {attribute} = ? WHERE {conditional}"

    with conn:
        conn.execute(query, (value,))
    conn.commit()

def read_data():
    for row in conn.execute(f"SELECT * FROM {TABLE_NAME}"): print(row)
    
def delete_data(): pass

def close_connection():
    conn.close()

def prep_insert_qry(args, colnames):
    """ source: https://stackoverflow.com/a/70745278
    this query is secure as long as `colnames` contains trusted data
    standard parametrized query mechanism secures `args`
    """

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
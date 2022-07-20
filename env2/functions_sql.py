
import sqlite3
import pandas as pd

database='./database/ot_clients.db'

def drop_sql_table(table_name):


    #Connecting to sqlite
    conn = sqlite3.connect('./database/ot_clients.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Doping EMPLOYEE table if already exists
    cursor.execute(f"DROP TABLE {table_name};")
    print("Table dropped... ")

    #Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()

def drop_column_from_table(table_name,column_name):

    #Connecting to sqlite
    conn = sqlite3.connect('./database/ot_clients.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    ##making sure column exists
    cursor.execute(f"SELECT * from {table_name}; ")
    if column_name in list(map(lambda x: x[0],cursor.description)):
    #Doping EMPLOYEE table if already exists
        try:
            cursor.execute(f"ALTER TABLE {table_name} DROP COLUMN {column_name}")
            print("Column dropped... ")
        except:
            print('No can not')
    else:
        print('Column not in table')

    #Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()

def get_tables_in_database(database):

    #Connecting to sqlite
    conn = sqlite3.connect(database)

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    print('TABLE NAMES', cursor.fetchall())
    #Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()

def drop_rows_table(table_name,column_name,condition):

    #Connecting to sqlite
    conn = sqlite3.connect('./database/ot_clients.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Droping rows by condition
    #query
    cursor.execute(f"DELETE FROM {table_name} where {column_name}={condition};")

    #Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()


def dataframe_to_sqltable(csv_file, table_name):

    #Connecting to sqlite
    conn = sqlite3.connect('./database/ot_clients.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    # Load CSV data into Pandas DataFrame
    df = pd.read_csv(csv_file)

    for col in df:
        if 'Unnamed' in col:
            df=df.drop(col,axis=1)

    # Write the data to a sqlite db table
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Run select sql query
    cursor.execute(f'select * from {table_name}')

    # Fetch all records
    # as list of tuples
    records = cursor.fetchall()

    # Display result
    for row in records[:3]:
        # show row
        print(row)

    #Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()

def rename_table(old_name,new_name):

    #Connecting to sqlite
    conn = sqlite3.connect('./database/ot_clients.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    #query
    cursor.execute(f"ALTER TABLE {old_name} RENAME TO {new_name};")
    print('Name changed...')
    #Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()

def get_n_last_records_from_table(table_name,n):

    #Connecting to sqlite
    conn = sqlite3.connect('./database/ot_clients.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    #query
    cursor.execute(f"""SELECT first_name,last_name, oid,ei_number FROM {table_name}
                    where oid in (select oid from {table_name} order by oid desc LIMIT {n});""")
    print(cursor.fetchall())
    #Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()

def get_records_with_filter(table_name,column_name,condition):


    #Connecting to sqlite
    conn = sqlite3.connect('./database/ot_clients.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    #query
    cursor.execute(f"SELECT first_name,last_name FROM {table_name} where {column_name}={condition};")
    print(cursor.fetchall())
    #Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()

def change_datatype_column(table_name,column_name,datatype):

    #Connecting to sqlite
    conn = sqlite3.connect('./database/ot_clients.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    #query
    cursor.execute(f"ALTER TABLE {table_name} ALTER COLUMN {column_name} {datatype};")
    print(f"Casting {column_name}...")
    #Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()

def sqltable_to_dataframe(table_name):
    #Connecting to sqlite
    conn = sqlite3.connect('./database/ot_clients.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    #query
    cursor.execute(f"select * from {table_name};")
    cols = [column[0] for column in cursor.description]
    #Comit your changes
    conn.commit()
    #Close the connection
    conn.close()

    return pd.DataFrame.from_records(data=cursor.fetchall(),columns=cols)

def changing_column_dtype(table_name,column_name,datatype):

    df=sqltable_to_dataframe(table_name)
    df[column_name]=df[column_name].fillna(0)
    df[column_name]=df[column_name].astype(datatype)
    df[column_name]=[x.split('.')[0] for x in df[column_name]]

    conn = sqlite3.connect('./database/ot_clients.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    df.to_sql(table_name, conn, if_exists='replace', index=False)

    #Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()
def getting_column_names(table_name):

    conn = sqlite3.connect('./database/ot_clients.db')

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    #query
    cursor.execute(f"select * from {table_name};")
    cols = [column[0] for column in cursor.description]
    #Comit your changes
    conn.commit()
    #Close the connection
    conn.close()

    return cols

"""
clients columns
['index', 'agency', 'activity', 'reception_date', 'dob', 'ei_number', 'age', 'execution_date', 'first_name', 'last_name', 'middle_name', 'address', 'ap
t', 'city', 'zip_code', 'parent', 'email']
"""

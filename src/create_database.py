#=================================================================#
#=======================> Create Database <=======================#
#=================================================================#

#=====> Import modules
# SQLite
import sqlite3
from sqlite3 import Error

# System modules
import os
import sys

# Data modules
import pandas as pd
from tabulate import tabulate

#=====> Define functions
# Make a query
def query(sql_query, dbpath):
    # open connection
    conn = sqlite3.connect(dbpath)
    # Get response
    response = pd.read_sql_query(sql_query, conn)
    # Close connection
    conn.close()
    
    return response

def pretty_query(sql_query, dbpath):
    # Query
    response = query(sql_query, dbpath)
    # Print
    print(tabulate(response, headers = 'keys', tablefmt = 'psql', showindex=False))

# Check if table exists 
def table_check(table, response):
    # Check
    if table in response["name"].values:
        print(f"[error] table \"{table}\" already exists.")
        sys.exit()
    else: 
        pass

# Try to query database
def try_check(table, dbpath):
    response = None
    # Try if query gets a response 
    try:
        response = query("SELECT name FROM sqlite_master;", dbpath)
    # Do nothing if fails
    except: 
        pass
    # Check table if succeeds
    finally:
        if response is not None:
            table_check(table, response)
    

# Load CSV-file
def load_csv(filename):
    # filepath 
    filepath = os.path.join("data", filename)
    # Load 
    df = pd.read_csv(filepath)
    
    return df

# Create table
def create_table(dbpath, table):
    # Define table 
    sql_create_table = f""" CREATE TABLE IF NOT EXISTS {table} (
                            id INT PRIMARY KEY NOT NULL, 
                            name TEXT NOT NULL,
                            mfr TEXT NOT NULL,
                            type BINARY,
                            calories INT,
                            protein INT,
                            fat INT,
                            sodium INT,
                            fiber FLOAT,
                            carbo FLOAT,
                            sugars INT,
                            potass INT,
                            vitamins INT,
                            shelf INT,
                            weight FLOAT,
                            cups FLOAT
                                    ); """

    # Connection
    conn = sqlite3.connect(dbpath)
    # Cursor 
    c = conn.cursor()
    
    # Create table & close 
    c.execute(sql_create_table)
    c.close()

    # Commit & close 
    conn.commit()
    conn.close()

# Append to table 
def append_table(dbpath, table, df, type_dict):
    # Connection
    conn = sqlite3.connect(dbpath)
    
    # Add data
    # to_sql
    df.to_sql(table, conn, if_exists="append", index=False, dtype=type_dict)

    # Close
    conn.close()

#=====> Define main()
def main():
    # > Definitions 
    # Path to database
    dbpath = os.path.join("db", "cereal_database.db")
    # Table 
    table = "cereals"
    # Data types 
    type_dict = {
        "id": "TEXT",
        "name": "TEXT", 
        "mfr": "TEXT",
        "type": "BINARY",
        "calories": "INT", 
        "protein": "INT",
        "fat": "INT",
        "sodium": "INT",
        "fiber": "FLOAT",
        "carbo": "FLOAT",
        "sugars": "INT",
        "potass": "INT",
        "vitamins": "INT",
        "shelf": "INT", 
        "weight": "FLOAT",
        "cups": "FLOAT"
    }
    
    # Check if table and database aready exists
    try_check(table, dbpath)
    
    # Load data 
    df = load_csv("cereal_clean.csv")
    
    # Create Table
    create_table(dbpath, table)
    
    # Append data to table
    append_table(dbpath, table, df, type_dict)
    
    # > Print info
    print("[info] Database created!")
    # No. rows
    pretty_query(f"SELECT COUNT(*) AS nr_row FROM {table};", dbpath)
    # Column info
    pretty_query(f"PRAGMA TABLE_INFO({table});", dbpath)

# Run main() function from terminal only
if __name__ == "__main__":
    main()    
    
#===========================================================================================#
#====================================> API code script <====================================#
#===========================================================================================#

#=====> Import modules
from typing import Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Path
from fastapi.responses import ORJSONResponse

# SQLite
import sqlite3
from sqlite3 import Error

# Data 
import pandas as pd

# System
import os
import sys
import orjson


#=====> It would have been better with ORM, but I don't have time
#=====> Define functions (This is not ideal, but it is what I can do)

# Define function that gets path to database
def dbpath():
    # Get path 
    dbpath = os.path.join("..", "db", "cereal_database.db")
    
    return dbpath

# Define query function 
def query(sql_query, dbpath):
    # open connection
    conn = sqlite3.connect(dbpath)
    # Get response
    response = pd.read_sql_query(sql_query, conn)
    # Close connection
    conn.close()
    
    return response.to_dict('index')

# Define function that gets nr. of rows in dataset
def get_max():
    # Get highest ID  
    maximum = query("SELECT MAX(id) FROM cereals;", dbpath())[0]["MAX(id)"]
    
    return maximum

# Define function that gets all ids
def get_ids():
    # Get ids
    all_ids = pd.DataFrame.from_dict(query("SELECT id FROM cereals;", dbpath()), 
                                     orient='index')["id"]
    
    return all_ids

# Define function that assembles a list of parameters
def assemble_list(param_dict):
    # Initiate list of parameters
    param_list = []
    
    # for each parameter...
    for key in param_dict:
        # Check if they have a value
        if param_dict[key]:
            # If string, add quotations
            if isinstance(param_dict[key], str):
                value = f"\"{param_dict[key]}\""
            else: 
                value = str(param_dict[key])  

            # Join pairs
            value_pair = " = ".join([key, value])
            # Append list
            param_list.append(value_pair)
    
    return param_list

# Define function that assembles a WHERE clause
def get_where(param_dict):
    # Get param_list
    param_list = assemble_list(param_dict)
    # Join list
    where_list = " AND ".join(param_list)
    # Get query
    sql_query = f"SELECT * FROM cereals WHERE {where_list};"
    
    return sql_query

# Define function that assembles a SET clause
def get_set(param_dict):
    # Get param_list
    param_list = assemble_list(param_dict)
    # Join subset of list
    set_list = ", ".join(param_list[1:])
    # Get query
    sql_query = f"UPDATE cereals SET {set_list} WHERE {param_list[0]};"
    
    return sql_query

# Define update function
def update_query(sql_query, dbpath):
    # Make connection
    conn = sqlite3.connect(dbpath)
    # Make cursor
    cur = conn.cursor()
    
    # Execute query
    cur.execute(sql_query)
    # Commit query
    conn.commit()
    
    # Close cursor 
    cur.close()
    # Close connection 
    conn.close()
    
# Define function that assigns id
def assign_id(body_dict):
    # Dict to dataframe
    add_on = pd.DataFrame(body_dict, index = [0])
    # Assign id 
    add_on["id"] = get_max() + 1
    
    return add_on
    
# Define functions that appends to table 
def append_table(df, dbpath):
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
    
    # Connection
    conn = sqlite3.connect(dbpath)
    
    # Add data
    # to_sql
    df.to_sql("cereals", conn, if_exists="append", index=False, dtype=type_dict)

    # Close
    conn.close()

#=====> Pydantic models
class Cereal(BaseModel):
    id: int | None = None
    name: str
    mfr: str
    type: str | None = None
    calories: int | None = None
    protein: int | None = None
    fat: int | None = None
    sodium: int | None = None 
    fiber: float | None = None
    carbo: float | None = None
    sugars: int | None = None 
    potass: int | None = None 
    vitamins: int | None = None 
    shelf: int | None = None 
    weight: float | None = None 
    cups: float | None = None

#=====> Initiate app
app = FastAPI(default_response_class=ORJSONResponse)

#=====> Define endpoints

@app.get("/")
async def root():
    # Query metadata
    response = query("PRAGMA TABLE_INFO(cereals);", dbpath())
    
    return response

@app.get("/cereals")
async def get_cereals(
    id: str | None = None,
    name: str | None = None,
    mfr: str | None = None,
    type: str | None = None,
    calories: int | None = None,
    protein: int | None = None,
    fat: int | None = None,
    sodium: int | None = None, 
    fiber: float | None = None,
    carbo: float | None = None,
    sugars: int | None = None, 
    potass: int | None = None, 
    vitamins: int | None = None, 
    shelf: int | None = None, 
    weight: float | None = None, 
    cups: float | None = None
):
    # Get parameters 
    param_dict = locals()
    
    # If parameters are specified...
    if any(list(param_dict.values())):
        # Get WHERE clause
        sql_query = get_where(param_dict)
    else:
        # Otherwise define a plain query
        sql_query = "SELECT * FROM cereals;"

    # Query with or without parameters
    response = query(sql_query, dbpath())
    
    return response

@app.get("/cereals/{cereal_id}")
async def get_cereal_id(
    cereal_id: Annotated[int, Path(title="The ID of the cereal to get", gt = 0, le = get_max())]
):
    # Query by id 
    response = query(f"SELECT * FROM cereals WHERE id = {cereal_id}", dbpath())
    
    return response

@app.post("/post/")
async def post_cereal(cereal: Cereal):
    # Get parameters from body
    cereal_dict = cereal.dict()
   
    # Give error message is body is more than a single row
    if any(isinstance(i,dict) for i in cereal_dict):
        response = {"loc": "body", 
                    "msg": "Request body cannot be a nested dictionary"}
    
    # If body is a single row...
    else:
        # If id is specified...
        if cereal_dict["id"]:
            # give error message if it exists in table
            if cereal_dict["id"] not in get_ids():
                response = {"loc": "body", 
                            "msg": "id does not exist - leave id empty, and id will be assigned"}
            
            # Update item if id exists
            else:
                # Update
                sql_query = get_set(cereal_dict)
                update_query(sql_query, dbpath())
                
                # Give response
                updated_id = cereal_dict["id"]
                response = query(f"SELECT * FROM cereals WHERE id = {updated_id};", dbpath())
        
        # If id is not spefified...
        else:
            # Assign new id
            add_on = assign_id(cereal_dict)
            
            # Append to table 
            append_table(add_on, dbpath())
            
            # Define response as new row
            new_id = add_on["id"][0]
            response = query(f"SELECT * FROM cereals WHERE id = {new_id};", dbpath())
    
    return response

   
# Cereal API
This is an attempt at creating an API as a solution to the Cereal Assignment on Specialisterne Academy (Spring 2023). The API Should allow a user to request data from a CSV file containing information on different cereals.

## Design considerations
I did not manage to finish the entire assignment, but I did manage to solve the following tasks: 

### Create database
> Create a database with data from 'cereal.csv'. Feel free to write a parser for the data so that you can insert additional data in the same format.

To create the database, I wrote to scripts: One to assign IDs to each cereal and parse the data so it becomes easier to feed foreward, and one to create a local SQLite database. 

### Simple GET requests
> Make an endpoint where you can make GET requests on ID and without ID to get all objects.

When the `/cereals` endpoint is called, the API responds with the entire dataset. Data for a single cereal can be requested by extending the endpoint with a cereal ID like so: `{host}/cereals/1`    
Specifying an ID number not present in the data will yield an error message.    
Making a GET request on the root directory will give metadata about the SQL cereals table as a response.  

### Add filtering
> Add filtering to GET requests, so you can send parameters like:    
'/results?calories=120' which should return all cereals that have exactly 120 kcal per 100 grams.    
You must be able to do this on all categories that belong to a given type of breakfast product.

The `/cereals` endpoint supports the following 16 query parameters, all of them optional:    

id _(str)_, name _(str)_, mfr _(str)_, type _(str)_, calories _(int)_, protein _(int)_, fat _(int)_, sodium _(int)_, fiber _(float)_, carbo _(float)_, sugars _(int)_, potass _(int)_, vitamins _(int)_, shelf _(int)_, weight _(float)_, cups _(float)_    

This can be done like so: `{host}/cereals?fat=1&sugars=3`    
The order of the parameters is not meaningful. 

### POST Requests
> Add POST requests to your endpoint. It must accept data in the same format as the GET request returns.    
If called with an ID, the program must check to see if the object exists, and if so, update it.    
If the object is not found, an error must be sent stating that you cannot choose the ID for new objects yourself.    
If you want to create a new object, a POST request without an ID must be sent.    

The post requests work according to the task-specifications. All columns except _name_ and _mfr_ are optional.       
A post request to this endpoint: `{host}/post`    

With the following body:
```
{
    "name": "Best Cereal Ever",
    "mfr": "Me",
    "type": "C"
}
```
Would add a new row with the specified parametersand assign it ID not already occupied in the database. The parameters not specified would ba assigned a _Null_ value.
The response would be a view of the newly added row. 
The API expects the parameters in the request body to have the following types:    

| Parameter | type  | Optional |
| --------- | ----- | -------- |
| id        | int   | Yes      |
| name      | str   | No       |
| mfr       | str   | No       |
| type      | str   | Yes      |
| calories  | int   | Yes      |
| protein   | int   | Yes      |
| fat       | int   | Yes      |
| sodium    | int   | Yes      | 
| fiber     | float | Yes      |   
| carbo     | float | Yes      |
| sugars    | int   | Yes      | 
| potass    | int   | Yes      | 
| vitamins  | int   | Yes      | 
| shelf     | int   | Yes      | 
| weight    | float | Yes      | 
| cups      | float | Yes      |

## Repository Structure
- __:file_folder: api:__ Folder for API code
    - main.py: script that creates the API

- __:file_folder: Data:__ Folder for input data to add to the database
- __:file_folder: db:__ Folder for .db (database) file 
- __:file_folder: src:__ Folder for python scripts for the database
    - create_database.py: Creates the database and adds the data from the csv file to as a table. Will yield an error message if a _cereal_database.db_ file already exists in the _db_ folder. 
    - data_cleaning.py: Cleans data and assigns ID to cereals.
    
- __:page_facing_up: .gitignore__
- __:page_facing_up: requirements.txt__

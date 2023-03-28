# Cereal API
This is an attempt at creating an API as a solution to the Cereal Assignment on Specialisterne Academy (Spring 2023). The API Should allow a user to request data from a CSV file containing information on different cereals.

## Design considerations
I did not manage to finish the entire assignment, but I did manage to solve the following tasks: 




```
{host}/cereals/1
```
25
Specifying an ID number not present in the data will yield an error message.    
26
Making a GET request on the root directory will give metadata about the SQL cereals table as a response.  
27
​
28
### Add filtering
29
> Add filtering to GET requests, so you can send parameters like:    
30
'/results?calories=120' which should return all cereals that have exactly 120 kcal per 100 grams.    
31
You must be able to do this on all categories that belong to a given type of breakfast product.
32
​
33
The _/cereals_ endpoint supports the following 16 query parameters, all of them optional:    
34
​
35
id _(str)_, name _(str)_, mfr _(str)_, type _(str)_, calories _(int)_, protein _(int)_, fat _(int)_, sodium _(int)_, fiber _(float)_, carbo _(float)_, sugars _(int)_, potass _(int)_, vitamins _(int)_, shelf _(int)_, weight _(float)_, cups _(float)_    
36
​
37
This can be done like so: 
38
```
39
{host}/cereals?fat=1&sugars=3
40
```
41
The order of the parameters is not meaningful. 
42
​
43
### POST Requests
44
> Add POST requests to your endpoint. It must accept data in the same format as the GET request returns.    
45
If called with an ID, the program must check to see if the object exists, and if so, update it.    
46
If the object is not found, an error must be sent stating that you cannot choose the ID for new objects yourself.    
47
If you want to create a new object, a POST request without an ID must be sent.    
48
​
49
The post requests work according to the task-specifications. All columns except _name_ and _mfr_ are optional.       
50
A post request to this endpoint:    
51
```
52
{host}/post
53
```
54
With the following body:
55
```
56
{
57
    "name": "Best Cereal Ever",
58
    "mfr": "Me",
59
    "type": "C"
60
}
61
```
62
Would add a new row with the specified parametersand assign it ID not already occupied in the database. The parameters not specified would ba assigned a _Null_ value.
63
The response would be a view of the newly added row. 
64
  The API expects the parameters in the request body to have the following types:    
65
​
66
| Parameter | type | Optional |
67
| --- | --- | --- |
68
| id | int | Yes |
69
| name | str | No |
70
| mfr | str | No |
71
| type | str | Yes |
72
| calories | int | Yes |
73
| protein | int | Yes |
74
| fat | int | Yes |
75
| sodium | int | Yes | 
76
| fiber | float | Yes |
77
| carbo | float | Yes |
78
| sugars | int | Yes | 
79
| potass | int | Yes | 
80
| vitamins | int | Yes | 
81
| shelf | int | Yes | 
82
| weight | float | Yes | 
83
| cups | float | Yes |

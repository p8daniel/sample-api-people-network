# API for a social network

API for a social network that will be able to manage any number of People and capture different types of relationships between them

For each People the system will record 3 informations
- First name
- Last name
- Nickname (Optional)

Between 2 People the system is able to capture two types of relationships
- Friendship information (a friendship will automatically be bi-directional)
- Family information (parent, kid)

In additional to the CRUD endpoints to manage People and their relationships, the system expose 2 endoint to query:
- All ancestors for a given person
- All family’s friends of any given person. (family’s friend is defined as someone who’s friend with any member of your family)


## Technical Stack

- FastAPI for the web server
- Neo4j for the database
- The standard Neo4j library is used to interact with the database (no OGM) https://neo4j.com/docs/api/python-driver/current/


## How to use

To launch the infrastructure needed (database), we use Docker and Docker-compose :

```
$ docker-compose up -d
```


## Data

The database can be initialized with 46 persons with their Parent/Children information, separated in 5 different families, available in the `data.yml` file. To load the data to the database run the python script in app/dp/init_dp.py should be launched.

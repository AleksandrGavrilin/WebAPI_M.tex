_____
This project is an asynchronous Web API service, which is implemented using: FastAPI, Pydantic, PostgreSQL.
_____
### <span style='color:rgb(250, 128, 114)'> Main functionality of the program: </span>
This project consists of three services:
1. Client (file client.pу);
2. Web (file api.pу);
3. Background (file background.py).

#### Client: ####
The service generates text like: '{TP address} {HTTP method} {URI} {HTTP status code}' and
sends it to the Web API service with POST requests.

#### Web: ####
The service accepts as input a string like: '{IP address} {HTTP method} {URI} {HTTP status
code}', parses it and saves it into the PostgreSQL database, marking each line unique
ID and storage time. It also returns the result from the database upon request.

#### Background: ####
The service periodically receives GET data requests from the service's Web API and stores them in
file_standart.log

### <span style='color:rgb(250, 128, 114)'> Instructions for working with docker: </span>
The start settings for running containers are located in the docker-compose.yml file
The Dockerfile contains instructions for building service image.
#### Launch docker-compose:
1. docker-compose build
2. docker-compose up -d
#### Stop and remove Docker-compose containers:
3. docker-compose down
#### View information about running Docker-compose processes and logs:
4. docker-compose ps
5. docker-compose logs

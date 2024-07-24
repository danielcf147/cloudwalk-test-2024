# CloudWalk case teste

To start this project, you need to have Docker installed. To run the application, follow the commands below.

````
docker-compose build
docker-compose up

````
App1 has a localhost web page, which has a select file and upload button.

The route for App1 is:

````
http://localhost:5001/
````
App2 has a .env.example file. You need to create a .env file with the information from the example and include the sender's email and password, as well as the recipient's email.

App2 has a localhost web page, which has a select file and upload button.

App2 has two routes:

````
http://localhost:5002/
http://localhost:5002/metrics
````



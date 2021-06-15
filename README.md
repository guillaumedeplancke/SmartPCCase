# Smart PC Case

This is my first project in my bachelor degrees at [Howest MCT](https://www.mct.be). I made a controller for my PC which makes it possible to boot/shutdown the computer, control the fan speeds & led strips and read some stats like power usage and temperature all from a web app written in pure HTML, CSS and Javascript.



## Project structure:

### Frontend:

**Location:** /frontend

As mentioned above the frontend is written in HTML, CSS and Javascript. In that way you can run it on your webserver of your preference like Nginx or Apache2.



### Backend:

**Location:** /backend

Before you can run the app.py file you will need to install the dependencies, this can be done with the following command in the backend folder `pip3 install -r requirements.txt`

The endpoints for the API can be tested with postman. You can find a collection in the /postman folder. 😉



### Database:

**Location:** /database

All sensors and outputs are stored in a database to make everything modular. I prefer to use MariaDB and had not problems, but MySQL should also work fine.

You can find an .sql script in the database folder which you can then import with for example MySQLWorkbench by setting up a remote connection to Raspberry Pi the project runs on.



### Arduino:

**Location:** /arduino/ProjectOne-Arduion

An Arduino Nano is used in the project to read the analog values from the voltage and current sensors and to calculate the RMS value which can then be sent to the RPI over a Serial connection.



## Installation:

I made an instructable with all the instructions to recreate this project. 

Check it out here: https://www.instructables.com/Smart-PC-Case/


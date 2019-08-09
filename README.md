# Favorite things
This is an application aimed at allowing users keep track of their favorite things, the application allows users to create categories and then add any number of favorite things ranked under the categories.

# Setting up the project locally
To run this project on your local machine you need to have the following installed.
- [Python 3.7](https://www.python.org/downloads/release/python-374/)
- [Pipenv](https://pypi.org/project/pipenv/)
- [Postgres DB](https://www.postgresql.org/download/)

## Installing
* **Open a terminal/command prompt** on your computer and cd into your preferred path/location. 
* **Clone repo:** to do this, run the following command on your **terminal/command prompt.**
```
git clone https://github.com/justega247/favorite-things.git
```
## Backend
* **Navigate to the cloned directory**
* **Install dependencies:** To do this, run the following command:
```
pipenv install
```
* **Add the required environment variables:** Locate a file with the filename `.sample.env` in the root directory and copy its content into a new file you will create in the root directory of the cloned repo and give it a filename of `.env`. In the `.env` file specify the environmental variables.
```
NAME='database name'
USER='database user'
PASSWORD='database password'
HOST='database host'
PORT='port'
SECRET_KEY='django app secret key'
DEBUG=True (N.B only for development)
```
* Run the migrations
```
python manage.py migrate
```
* Load default categories
```
python manage.py loaddata category_fixture.json
```
* Start the application
```
python manage.py runserver
```
* You can run the tests using
```
python manage.py test
```
* On running the tests, a **cover** folder will be generated in the root directory. You can open any of the *.html files generated to view the coverage for that file or better still just open the index.html file to view all the test coverage.

## API Endpoints
| Request type | Endpoint | Actions |
| ------------ | -------- | ------- |
| POST         | /category | Create a category |
| GET          | /category | Get all the categories |
| GET          | /category/:categoryId | Get a category by its Id |
| POST         | /favorite | Create a favorite |
| GET          | /favorite/:favoriteId | Get a favorite thing by its Id |
| DELETE       | /favorite/:favoriteId | Delete a favorite thing by Id |
| PUT          | /favorite/:favoriteId | Update a favorite thing |
| GET          | /favorite/category/:categoryId | Get favorites under a category |
| GET          | /favorite/history/:favoriteId | Get audit for a favorite thing |

## Frontend
You'll need the following installed on your machine
- [ Nodejs](https://nodejs.org/en/)

* **Navigate to the client directory**
* **Install dependencies:** To do this, run the following command:
```
npm-install
```

* After installing all the dependencies, you can start the frontend of the applcation using
```
npm run serve
```

* Once the app has successfully been served, you can view it and start interacting with it in your browser at
```
http://127.0.0.1:8080
```

# Deploying on AWS
- Create an AWS account [here](https://aws.amazon.com/) if you do not already have one
- After successfully signing up/ login, create an EC2 instance and launch using the UBUNTU Server 16.04 LTS
- Click on Review and Launch
- Create a new Key pair.
- Enter the key pair name (e.g test)
- Download the key pair as it will be required to SSH to the server
- Finally click on Launch Instances

### Setting up the Server
- Open up a terminal and navigate to the directory where you saved the private key to
- Set the file permission of your private key e.g
```
sudo chmod 400 test.pem
```
- Obtain your server public DNS, You can find it by selecting your running instance & below that page in an window you will find “Public DNS” , Just Copy It.
- SSH to the server using
```
ssh -i test.pem ubuntu@public_DNS
```
- Add the following rules to the security group of your EC2 instsnce
```
Under the inbound rules section
- Type: HTTP, Port Range: 80
- Type: Custom TCP Rule, Port Range: 8000
N.B do not alter any other column
```
- Update and Upgrade the packages
```
sudo apt-get update && apt-get upgrade -y
```
- Install the necessary packages Python3.7, PostgreSQL, Nginx and Git
```
sudo apt-get install python3-pip python3.7-dev libpq-dev postgresql postgresql-contrib nginx git
```

- Clone the project
```
git clone https://github.com/justega247/favorite-things.git
```

- Create a database and a database user for the django app
- Create and Populate a .env file in the root directory of the project with the details of the database
```
sudo touch .env
```
- Then populate it with the necessary details
```
NAME='database name'
USER='database user'
PASSWORD='database password'
HOST='database host'
PORT='port'
SECRET_KEY='django app secret key'
DEBUG=True (N.B only for development)
```

- Navigate into the **client** folder and then into the **src** folder. In the **config/index.js**
```
sudo nano client/src/config/index.js
```
- In the file replace the public_DNS address with yours.

- Open the **favorite.conf** in the root directory
```
sudo nano favorite.conf
```
- Edit the file replacing {{ Public DNS }} with your own address same as in the `client/src/config/index.js`. N.B do not add `http://` to the address. E.g if the address is `http://ec2-31-18-220-65.us-east-2.compute.amazonaws.com`, you only need the `ec2-31-18-220-65.us-east-2.compute.amazonaws.com` part.

- Set the file permission for the deployment script to `read, write and execute`
```
sudo chmod 774 deploy.sh
```

Run the deployment script using
```
./deploy.sh
```
- **N.B** You'll be prompted a couple of times while the script is running to accept some conditions, go ahead and accept them.

- Once the deploy script has run completely, you can visit your public DNS address in your browser to view the deployed app and start interacting with it.

# Built With
1. Vuejs
2. Python 3.7
3. Django
4. Django Rest Framework
5. Postgres

# Author(s)
- Okeremeta Tega

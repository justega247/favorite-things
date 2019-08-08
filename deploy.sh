#!/bin/bash

sudo apt-get update && sudo apt-get upgrade -y

echo "Starting python installation...."
{
	sudo apt-get install python-pip -y
	sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt-get update
  sudo apt-get install python3.7 -y
  sudo apt-get install libpq-dev
  sudo apt-get install python3.7-dev
	echo "Python Installed :)"
} || {
	echo "Python installation failed"
}

echo "Installing pipenv..."
{
	pip3 install pipenv
	echo "Pipenv installed :)"
} || {
	echo "Pipenv installation failed"
}

echo "Installing server dependencies"
	pipenv run pipenv install
	pipenv run python manage.py makemigrations
	pipenv run python manage.py migrate
  pipenv run python manage.py loaddata category_fixture.json
echo "Dependencies installed and defaults added"

echo "Starting gunicorn"
{
  sudo apt-get install -y supervisor
  sudo touch /etc/supervisor/conf.d/gunicorn.conf
  sudo cp gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf
  sudo mkdir /var/log/gunicorn
  sudo supervisorctl reread 
  sudo supervisorctl update
  echo "gunicorn running"
} || {
  echo "gunicorn not running"
}


echo "Installing nodejs"
{
	curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash
  export NVM_DIR="$HOME/.nvm"
	[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
	[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
  nvm install node
	echo "Node installed :)"
} || {
	echo "Nodejs installation failed"
}

echo "Installing client dependencies"
cd client && npm install && cd -
echo "Dependencies installed :)"

echo "building client"
cd client && npm run build && cd -
echo "client built :)"


echo "Installing Nginx"
sudo apt-get install nginx -y
sudo touch /etc/nginx/sites-available/favorite_things
sudo cp favorite.conf /etc/nginx/sites-available/favorite_things

sudo ln -s /etc/nginx/sites-available/favorite_things /etc/nginx/sites-enabled/favorite_things

sudo cp nginx.conf /etc/nginx/nginx.conf
sudo nginx -t
sudo service nginx restart

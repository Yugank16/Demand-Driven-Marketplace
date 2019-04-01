# Demand Driven Marketplace

Demand driven marketplace for household items(old/new/2nd hand everything). Buyer will post their requirement with budget, where seller(any platform user) can bid for that requirement.

# System Requirements

1 psql (PostgreSQL) v9.5.14.

2 Python v2.7


# Django Setup (for ubuntu)

Open Terminal - Ctrl+Alt+T.

Type following commands- 

```bash
sudo apt-get update
```

1- Install pip-

	sudo apt-get install python-pip
	

2- Install and use virtual env wrapper
	
	
	sudo pip install virtualenvwrapper
	
	export WORKON_HOME=~/Envs
	
	mkdir -p $WORKON_HOME
	
	source /usr/local/bin/virtualenvwrapper.sh
	
	mkvirtualenv env1

	workon env1
	
put statements 2 & 4 in our ~/.bashrc file

3- Clone project to your directory

	git clone https://code.jtg.tools/induction-jan-19/demand-driven-marketplace.git

	cd ~/demand-driven-marketplace

4- Install all requirements. 

	pip install -r requirements.txt

5- Install redis (5.0.4) from this link https://redis.io/
	Unzip it to your directory and move to redis folder and type following command

	src/redis-server


# Start Project

1 Run following command and enter to the main directory.
	
	cd ~/demand_driven_marketplace_api/demand_driven_marketplace_api/

2 Add local_settings.py file in the directory where local_settings.py.template is stored 	and configure file with your details.

3- Go to stripe official website and register.
	https://dashboard.stripe.com/register

	After registering , get your public key and secret key and put it in local_settings.py	

# Run Project

1- Run $ celery -A demand_driven_marketplace_api worker -l info -B 

2- Run $ python manage.py migrate to run migrations.

3- Run server, $ python manage.py runserver.

4- Create Django Admin, in the terminal run $ python manage.py createsuperuser, fill in the required details.

5- Open http://127.0.0.1:8000/admin/ in your browser.



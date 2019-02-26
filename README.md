# Demand Driven Marketplace


Demand driven marketplace for household items(old/new/2nd hand everything). Buyer will post their requirement with budget, where seller(any platform user) can bid for that requirement.

# System Requirements

1 psql (PostgreSQL) v9.5.14.

2 Python v2.7.


# Django Setup (for ubuntu)

Open Terminal - Ctrl+Alt+T.

Type following commands- 

```bash
sudo apt-get update
```

1- Install pip-

	sudo apt-get install python-pip
	

2- Install Virtual Environment 

	
	sudo pip install virtualenv 
	

3- Install and use virtual env wrapper
	
	
	sudo pip install virtualenvwrapper
	
	export WORKON_HOME=~/Envs
	
	mkdir -p $WORKON_HOME
	
	source /usr/local/bin/virtualenvwrapper.sh
	
	mkvirtualenv env1

	workon env1

	Deactivate
	
	
	put statements 2 & 4 in our ~/.bashrc file

4- Install all requirements. Refer requirements.txt

# Start Project

1 Clone project to your directory.

2 Make a local_setting.py file 

3 Add local_settings.py file in the main directory where local_sttings.py.template is present, add the code from tempelate to local_settings.py after replacing all the placeholders.

4 Add the code from settings.py.template (present in same directory as in step 3) to the end of your settings.py file.

# Run Project

1- Run $ python manage.py migrate to run migrations.

2- Run server, $ python manage.py runserver.

3- Open http://127.0.0.1:8000/ in your browser.



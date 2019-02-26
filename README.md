# Demand Driven Marketplace


Demand driven marketplace for household items(old/new/2nd hand everything). Buyer will post their requirement with budget, where seller(any platform user) can bid for that requirement.

Requirements

Users: Any user can sign up as platform as buyer, seller or both. A user can invite more users at platform(invite via csv file also supported) but max. 25 users a day only. 
There can be multiple groups in our system. Any user can create a group and the owner can add one or more admins to the group.

Item:
A user can post their requirement as form of Item.

Item Bid: Any user can bid for that item requirement by providing product details(min. 6 photo and other details). Item requester can not view a bid price until a bid disclose.

Public Bid vs Group specific bid: An item requester can open the bid for all or specific to groups.

Eligible bidder: Before a bid disclose, item requester can reject a seller bid after viewing  product specification/details. Platform will refund bid amount in next 2 hours. 

Bid disclose: A eligible bidder/seller with minimum sell price will be selected as bid winner.

# Django Setup (for ubuntu)

0- sudo apt-get update

1- sudo apt-get install python-pip

2- pip install Django==1.11.20

3- You can use any editor to work. For Example, lets install  Visual Studio.

# Installing Visual Studio (Optional)

1 Download Visual Studio Code
  https://code.visualstudio.com/download
2 Install and Open Visual Code
3 In the extensions tab, download python extension.



#Start Project

1 Clone project to your directory.
2 Make a local_setting.py file where settings file is present and add the following code:

	import settings

	DATABASES = {
    		'default': {
			'ENGINE': '<Write your database engine>',
			'NAME': ' '<database name>',
			'USER': '<db user>',
			'PASSWORD': '<db password>',
			'HOST': '<your host>',
			'PORT': '<your port>',
    			}
		}

3 Add following code in the last of your settings.py file.

	try:
   		from local_settings import *
	except ImportError:
    		raise ImportError("A local_settings.py file is required to run this project")

# Run Project

1 Run $ python manage.py migrate to run migrations
2 Run server, $ python manage.py runserver
3 Open http://127.0.0.1:8000/ in your browser.



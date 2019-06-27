# Items-Catalog
Item-Catalog Project for Udacity's FullStack Nanodegree

# About
This application provides a list of items within a variety of categories as well as provide a user authentication system. Login users will have the ability to post, edit, and delete their own items.

# Features
1 Full CRUD support using SQLAlchemy and Flask.
2 JSON endpoints.
3 Implements oAuth using Google Sign-in API.

# To run this project:

1 Download and install [Vagrant](https://www.vagrantup.com/downloads.html).

2 Download and install [VirtualBox](https://www.virtualbox.org/wiki/Downloads).

3 Clone or download the Vagrant VM configuration file from [Udacity](https://github.com/udacity/fullstack-nanodegree-vm).

4 Open the above directory and navigate to the vagrant/ sub-directory.

5 Open your terminal in the same directory as you vagrant file

>vagrant up

This will cause Vagrant to download the Ubuntu operating system and install it. This may process may take quite a while depending on your Internet speed.

After the the installation completes, connect to the newly created VM by typing in yout terminal:

>vagrant ssh

To the shared repository type:

>cd/vagrant/

Download or clone this repository, and navigate to it.

Install or upgrade Flask:

sudo python3 -m pip install --upgrade flask
Set up the database:

python3 database_setup.py
Insert dummy values. If you don't run this, the application might not run.

python3 fake_db_populator.py
Run this application:

python3 app.py
Open http://localhost:5000/ in your favourite Web browser, and enjoy.

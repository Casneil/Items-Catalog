# Items-Catalog
Item-Catalog Project for Udacity's FullStack Nanodegree

# About
This application provides a list of items within a variety of categories as well as provide a user authentication system. Login users will have the ability to post, edit, and delete their own items.

# Features
- Full CRUD support using SQLAlchemy and Flask.
- JSON endpoints.
- Implements oAuth using Google Sign-in API.

# To run this project:

1. Download and install [Vagrant](https://www.vagrantup.com/downloads.html).

2. Download and install [VirtualBox](https://www.virtualbox.org/wiki/Downloads).

3. Clone or download the Vagrant VM configuration file from [Udacity](https://github.com/udacity/fullstack-nanodegree-vm).

4. Open the above directory and navigate to the vagrant/ sub-directory.

5. Open your terminal in the same directory as you vagrant file

          vagrant up

6. This will cause Vagrant to download the Ubuntu operating system and install it. This may process may take quite a while depending on your Internet speed.

7. After the the installation completes, connect to the newly created VM by typing in yout terminal:

          vagrant ssh

8. To the shared repository type:

          cd/vagrant/

9. Download or clone [this](https://github.com/Casneil/Items-Catalog) repository, and navigate to it.

10. Install or upgrade Flask:

          sudo python3 -m pip install --upgrade flask

11. Set up the database:

          python3 catalog_setup.py

12. This step is optional, you can add Shops, Items via your browser when the programm is already running.

          python3 catalog_add.py

13. Run this application:

          python3 application.py

14. In your favourite Web browser open (http://localhost:5000), and enjoy :+1:.

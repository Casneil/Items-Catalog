#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_setup import Base, User, Mall, Items

engine = create_engine('sqlite:///catalog.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
session.commit()


# Create a fake user
Casneil = User(name="Casneil Simpson", email="casneil.simpson@gmail.com",
               picture='https://www.facebook.com/photo.php?fbid=391170941\
                   236304&set=pb.100010302044120.-2207520000.1561525715\
                       .&type=3&theater')
session.add(Casneil)
session.commit()


# Making name of the shop Sport Wears with Items #

Casneil_Shops = Mall(user_id=1, department="Sport Wears",
                     description="All your Sporting needs!!")
session.add(Casneil_Shops)
session.commit()


Addidas = Items(user_id=1, name="Addidas Sport Max",
                description="Made withsport in mind",
                price="150 USD", mall=Casneil_Shops)

session.add(Addidas)
session.commit()


Puma = Items(user_id=1, name="Puma Preditor",
             description="Life is like a hunt, hunt smart with Preditor",
             price="350 USD",
             mall=Casneil_Shops)

session.add(Puma)
session.commit()


Addidas_Super_Sport = Items(user_id=1, name="Addidas Super Sport",
                            description="Making Sport more enjoyable",
                            price="150 USD", mall=Casneil_Shops)

session.add(Addidas_Super_Sport)
session.commit()


Lacosta = Items(user_id=1, name="Lacosta Goo",
                description="From passion comes innovation",
                price="100 USD", mall=Casneil_Shops)

session.add(Lacosta)
session.commit()


Casneil_Shops1 = Mall(user_id=1, department="Casual Wears",
                      description="Look and Feel Good wherever you go")

session.add(Casneil_Shops1)
session.commit()


Nike = Items(user_id=1, name="Nike Air Force 1",
             description="Retro Nike shoes made great by the great Legends",
             price="300 USD ", mall=Casneil_Shops1)

session.add(Nike)
session.commit()

Reebok = Items(user_id=1, name="Reebok Switch",
               description="Welcome to the 21st Century!",
               price="180 USD", mall=Casneil_Shops1)

session.add(Reebok)
session.commit()

Prada = Items(user_id=1, name="Prada La'voure",
              description="It takes more than just fashion it takes Prada",
              price="500 USD", mall=Casneil_Shops1)

session.add(Prada)
session.commit()


Lui_Vitton = Items(user_id=1, name="Lui Vitton",
                   description="This is it 21st Century!", price="600 USD",
                   mall=Casneil_Shops1)

session.add(Lui_Vitton)
session.commit()


Casneil_Shops2 = Mall(user_id=1,
                      department="Female & Male Pants,\
                      Shorts, Shirts, T-Shirts etc",
                      description="Look and Feel Good for any occasion!")
session.add(Casneil_Shops2)
session.commit()

Levi = Items(user_id=1, name="Levi's 501",
             description="Only two colors: Blue and Grey",
             price="50 USD", mall=Casneil_Shops2)

session.add(Levi)
session.commit()

H_n_M = Items(user_id=1, name="H&M White T-Shirt", description="White",
              price="15 USD",
              mall=Casneil_Shops2)

session.add(H_n_M)
session.commit()


Forever_21 = Items(user_id=1, name="Forever 21 Leggins",
                   description="Only three colors: Blue, Black and White",
                   price="10 USD", mall=Casneil_Shops2)
session.add(Forever_21)
session.commit()


Victoria_Secret = Items(user_id=1, name="Victoria's Secret",
                        description="Variety of colors",
                        price="8 USD", mall=Casneil_Shops2)

session.add(Victoria_Secret)
session.commit()


print ("Shops and Items added!")

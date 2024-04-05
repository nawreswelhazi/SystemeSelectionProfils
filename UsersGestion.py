# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 19:46:08 2023

@author: NAWRESS
"""

import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from LoginDB import *

engine = create_engine('sqlite:///users.db', echo=True)

# create a Session
"""Session = sessionmaker(bind=engine)
session = Session()"""


#user.password="password"
#user.username="username"
#user.isAdmin=0
#session.add(user)
# commit the record the database
#session.commit()

"""user.password="nawres"
user.username="nawres"
user.isAdmin=1
session.add(user)
# commit the record the database
session.commit()"""

def AddUser(username, name, familyname, password):
    Session = sessionmaker(bind=engine)
    session = Session()
    user = User()
    user.username=username
    user.name=name
    user.familyname=familyname
    user.password=password
    user.isAdmin=1
    session.add(user)
    session.commit()
    

#AddUser('nawres', 'nawres', 'welhazi', 'nawres')

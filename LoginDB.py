# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 19:42:23 2023

@author: NAWRESS
"""

from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True)
    name = Column(String)
    familyname = Column(String)
    password = Column(String)
    isAdmin = Column(Integer())

#Constructeur
def __init__(self, username, name, familyname, password, isAdmin):
    self.username = username
    self.name = name
    self.familyname = familyname
    self.password = password
    self.isAdmin = isAdmin

# create table
Base.metadata.create_all(engine)
    
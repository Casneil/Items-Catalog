#!/usr/bin/env python3

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    def __repr__(self):
        return f"User('{self.name}, '{self.email}', '{self.picture}')"


class Mall(Base):
    __tablename__ = 'mall'
    id = Column(Integer, primary_key=True)
    department = Column(String(80), nullable=False)
    description = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        return {
           'id': self.id,
           'department': self.department,
           'description': self.description, }


class Items(Base):
    __tablename__ = 'items'

    name = Column(String(80), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    id = Column(Integer, primary_key=True)
    mall_id = Column(Integer, ForeignKey('mall.id'))
    mall = relationship(Mall)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):

        return {
           'name': self.name,
           'description': self.description,
           'price': self.price,
           'id': self.id, }


# END OF FILE #
engine = create_engine('sqlite:///catalog.db')


Base.metadata.create_all(engine)

#!/usr/bin/python3
"""This module contains the DBStorage class definition.
The DBstorage class helps store data into the Database for the
AiRBnB project.
"""
import os
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


classes = {
        'BaseModel': BaseModel, 'User': User, 'Place': Place,
        'State': State, 'City': City, 'Amenity': Amenity,
        'Review': Review
}


class DBStorage:
    """Stores data into the mysql database.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes a new instance of the DBStorage class.

        Args: None

        Attributes:

        """
        user = os.environ['HBNB_MYSQL_USER']
        password = os.environ['HBNB_MYSQL_PWD']
        host = os.environ['HBNB_MYSQL_HOST']
        database = os.environ['HBNB_MYSQL_DB']
        url = f"mysql+mysqldb://{user}:{password}@{host}/{database}"
        self.__engine = create_engine(url, pool_pre_ping=True)
        Base.metadata.bind = self.__engine

        try:
            if os.environ['HBNB_ENV'] == 'test':
                Session = sessionmaker(bind=self.__engine)
                self.__session = Session()
                Base.metadata.drop_all(self.__engine)
                self.__session.close()
        except KeyError:
            pass

    def all(self, cls=None):
        """queries the current database session for all objects
        or objects of the class specified in cls.
        """
        dictionary = {}
        if cls and cls in classes:
            objs = self.__session.query(classes[cls]).all()
            for obj in objs:
                key = f"{cls}.{obj.id}"
                dictionary.update({key: obj})
        else:
            for key, val in classes.items():
                objs = self.__session.query(val).all()
                for obj in objs:
                    key1 = f"{key}.{obj.id}"
                    dictionary.update({key1: obj})

        return dictionary

    def new(self, obj):
        """adds the object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """commits all changes of the current databse session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from the current database session,
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """creates all tables in the database and creates the
        current database session made use in the entirety of
        the program's execution.
        """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                 expire_on_commit=False))
        self.__session = Session()

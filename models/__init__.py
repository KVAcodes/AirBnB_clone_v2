#!/usr/bin/python3
"""This module instantiates an object of class FileStorage
or DBStorage class if env variable HBNB_TYPE_STORAGE equals db"""

import os
from .user import User
from .place import Place
from .state import State
from .city import City
from .amenity import Amenity
from .review import Review

__all__ = ['User', 'Place', 'State', 'City', 'Amenity', 'Review']

if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
    storage.reload()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
    storage.reload()

#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models.state import State
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
import os
os.environ['HBNB_TYPE_STORAGE'] = 'db'
if os.getenv('HBNB_TYPE_STORAGE') == 'db':
	storage = DBStorage()
else:
	storage = FileStorage()

states = [state.id for state in storage.all(State).values()]
print(states)



#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models.user import User
import os

kwargs = {"name":"johnnie", "password":"herty"}
u = User(**kwargs)
print(u.to_dict())



#!/usr/bin/python3
"""User clss"""
from models.base_model import BaseModel


class User(BaseModel):
    """user obj"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""

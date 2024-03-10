#!/usr/bin/python3
"""BaseModel class"""
import models
import uuid
from datetime import datetime
class BaseModel:
    """the method of Base Model class"""
    def __init__(self, *args, **kwargs ):
        """initializes Base Class"""
        for key, value_num in kwargs.items():
            if kwargs:
                for key, value_num in kwargs.items():
                date_format = "%Y-%m-%dT%H:%M:%S.%f"
                if key == "created_at" or key == "updated_at":
                  self.__dict__[key] = datetime.strptime(value_num, date_format)
                else:
                  self.__dict__[key] = value_num

            else:
                self.id = str(uuid.uuid4())
                self.created_at = datetime.now()
                self.updated_at = datetime.now()
    def __str__(self):
        """overriding"""
        return "[{}] ({}) {}".format(self.__class__.__name__, self.id, self.__dict__)
    def save(self):
        """updated_at attribute to the now datetime"""
        self.updated_at = datetime.now()
    def to_dict(self):
        """returns a dictionary representation __dict__ of the instance"""
        in_dict = self.__dict__.copy()
        in_dict["updated_at"] = self.updated_at.isoformat()
        in_dict["created_at"] = self.created_at.isoformat()
        in_dict["__class__"] = self.__class__.__name__
        return in_dict

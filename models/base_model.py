#!/usr/bin/python3
"""BaseModel class"""
import models
import uuid
from datetime import datetime


class BaseModel:
    """the method of Base Model class"""

    def __init__(self, *args, **kwargs):
        """initializes Base Class"""
        if kwargs is not None and kwargs != {}:
            for key in kwargs:
                if key == "created_at":
                    self.__dict__["created_at"] = datetime.strptime(
                        kwargs["created_at"], "%Y-%m-%dT%H:%M:%S.%f"
                    )
                elif key == "updated_at":
                    self.__dict__["updated_at"] = datetime.strptime(
                        kwargs["updated_at"], "%Y-%m-%dT%H:%M:%S.%f"
                    )
                else:
                    self.__dict__[key] = kwargs[key]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            storage.new(self)

    def __str__(self):
        """overriding"""
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """updated_at attribute to the now datetime"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns a dictionary representation __dict__ of the instance"""
        in_dict = self.__dict__.copy()
        in_dict["__class__"] = type(self).__name__
        in_dict["created_at"] = in_dict["created_at"].isoformat()
        in_dict["updated_at"] = in_dict["updated_at"].isoformat()
        return in_dict

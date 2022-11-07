import datetime

from sqlalchemy import (
    VARCHAR,
    Column,
    Date,
    Integer,
)
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()


class Groups(BaseModel):

    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    iiko_id = Column(VARCHAR(500), nullable=False)
    name = Column(VARCHAR(500), nullable=False)

    def __str__(self):
        return self.name

    def __init__(self, iiko_id: str, name: str):
        self.name = name
        self.iiko_id = iiko_id

import datetime

import sqlalchemy
from sqlalchemy import (
    VARCHAR,
    Column,
    Date,
    Integer, ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

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


association = sqlalchemy.Table(
    "association", BaseModel.metadata,
    Column("product_id", ForeignKey("products.id")),
    Column("basket_id", ForeignKey("baskets.id")),
)


class Product(BaseModel):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(300), nullable=False)
    group = Column(Integer, ForeignKey("groups.id"))


class Basket(BaseModel):

    __tablemane__ = "baskets"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    products = relationship("Product", secondary="association")

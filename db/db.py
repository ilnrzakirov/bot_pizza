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
    Column("count", Integer),
)


association_mod = sqlalchemy.Table(
    "association_mod", BaseModel.metadata,
    Column("product_id", ForeignKey("products.id")),
    Column("modifications_id", ForeignKey("modifications.id")),
)

class Product(BaseModel):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(300), nullable=False)
    group = Column(Integer, ForeignKey("groups.id"))
    image = Column(VARCHAR(500), nullable=True)
    price = Column(Integer, nullable=False, default=0)
    modification = relationship("Modification", secondary="association_mod")


class Basket(BaseModel):

    __tablename__ = "baskets"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    products = relationship("Product", secondary="association")


class Modification(BaseModel):

    __tablename__ = "modifications"

    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(300), nullable=False)
    price = Column(Integer, nullable=False, default=0)

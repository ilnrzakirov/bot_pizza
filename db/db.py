import sqlalchemy
from sqlalchemy import (
    VARCHAR,
    Column,
    Integer,
    ForeignKey
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
    product_id = Column(VARCHAR(300), nullable=False)
    name = Column(VARCHAR(300), nullable=False)
    group = Column(Integer, ForeignKey("groups.id"), nullable=True)
    image = Column(VARCHAR(500), nullable=True)
    price = Column(sqlalchemy.types.Float, nullable=False, default=0)
    modification = relationship("Modification", secondary="association_mod")
    weight = Column(sqlalchemy.types.Float, nullable=True)
    description = Column(VARCHAR(1200), nullable=True)
    mod_group = Column(VARCHAR(500), nullable=True)

    def __str__(self):
        return self.name

    def __init__(self, name: str, group_id: int, image_url: str,
                 price: float, product_id: str, description: str,
                 mod_group: str, weight: float = 0):
        self.name = name
        self.group = group_id
        self.image = image_url
        self.price = price
        self.product_id = product_id
        self.weight = weight
        self.description = description
        self.mod_group = mod_group


association_mod_basket = sqlalchemy.Table(
    "association_mod_basket", BaseModel.metadata,
    Column("baskets_id", ForeignKey("basket_mod.id")),
    Column("modifications_id", ForeignKey("modifications.id")),
)

association_prod_basket = sqlalchemy.Table(
    "association_prod_basket", BaseModel.metadata,
    Column("baskets_id", ForeignKey("basket_mod.id")),
    Column("product_id", ForeignKey("products.id")),
)

basket_mod_association = sqlalchemy.Table(
    "basket_mod_association", BaseModel.metadata,
    Column("baskets_id", ForeignKey("baskets.id")),
    Column("baskets_mod_id", ForeignKey("basket_mod.id")),
)


class BasketMod(BaseModel):
    __tablename__ = "basket_mod"

    id = Column(Integer, primary_key=True)
    products = relationship("Product", secondary="association_prod_basket")
    modifications = relationship("Modification", secondary="association_mod_basket")


class Basket(BaseModel):

    __tablename__ = "baskets"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, nullable=False)
    # products = relationship("Product", secondary="association")
    # modifications = relationship("Modification", secondary="association_mod_basket")
    products = relationship("BasketMod", secondary="basket_mod_association", cascade="all,delete")
    count = Column(Integer, nullable=False, default=0)
    price = Column(sqlalchemy.types.Float, nullable=False, default=0)

    def __str__(self):
        return self.id

    def __init__(self, chat_id: int, count: int = 0, price: float = 0):
        self.chat_id = chat_id
        self.count = count
        self.price = price


class Modification(BaseModel):

    __tablename__ = "modifications"

    id = Column(Integer, primary_key=True)
    mod_id = Column(VARCHAR(300), nullable=False)
    name = Column(VARCHAR(300), nullable=False)
    price = Column(sqlalchemy.types.Float, nullable=False, default=0)
    weight = Column(sqlalchemy.types.Float, nullable=False)
    group = Column(VARCHAR(300), nullable=False)
    type = Column(VARCHAR(500), nullable=False)

    def __str__(self):
        return self.name

    def __init__(self, name: str, price: float, mod_id: str,
                 mod_type: str, group_id: int,  weight: float = 0,):
        self.name = name
        self.price = price
        self.mod_id = mod_id
        self.weight = weight
        self.type = mod_type
        self.group = group_id

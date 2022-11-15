import sqlalchemy

from db.db import Product, Groups
from settings import session_maker
from sqlalchemy import select


async def get_product_by_group_id(group: Groups) -> list[Product]:
    session = session_maker()
    query = sqlalchemy.select(Product).where(Product.group == group.id)
    product_list = []
    products = await session.execute(query)
    for product in products:
        product_list.append(product[0])
    return product_list

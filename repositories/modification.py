import sqlalchemy

from db.db import Product, Modification
from settings import session_maker
from sqlalchemy import select


async def get_product_by_group_id(product: Product) -> list[Modification]:
    session = session_maker()
    query = sqlalchemy.select(Modification).where(Modification.product_id == product.id)
    modification_list = []
    modifications = await session.execute(query)
    for modification in modifications:
        modification_list.append(modification[0])
    return modification_list

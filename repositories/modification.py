import sqlalchemy

from db.db import Product, Modification
from settings import session_maker


async def get_modifications_by_product_id(product: Product) -> list[Modification]:
    session = session_maker()
    query = sqlalchemy.select(Modification).where(Modification.product_id == product.id)
    modification_list = []
    modifications = await session.execute(query)
    await session.close()
    for modification in modifications:
        modification_list.append(modification[0])
    return modification_list

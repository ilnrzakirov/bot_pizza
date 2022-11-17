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


async def get_modifications_by_mod_id(id_in: str):
    session = session_maker()
    query = sqlalchemy.select(Modification).where(Modification.group == id_in)
    data = await session.execute(query)
    mod_list = []
    for mod in data:
        mod_list.append(mod[0])
    await session.close()
    return mod_list

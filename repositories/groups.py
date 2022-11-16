from sqlalchemy import select

from db.db import Groups, Product
from settings import session_maker


async def get_groups_list() -> list[Groups]:
    session = session_maker()
    group_list = await session.execute(select(Groups))
    return group_list


async def get_group_by_id(id_in: str) -> Groups | None:
    session = session_maker()
    groups = await get_groups_list()
    session.close()
    for group in groups:
        if id_in in group[0].iiko_id:
            return group[0]
    return None


async def get_products_list() -> list[Product]:
    session = session_maker()
    product_list = await session.execute(select(Product))
    return product_list


async def get_product_by_id(id_in: str) -> Product | None:
    session = session_maker()
    products = await get_products_list()
    session.close()
    for product in products:
        if id_in in product[0].product_id:
            return product[0]
    return None

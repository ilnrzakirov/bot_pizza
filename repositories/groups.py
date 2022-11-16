from sqlalchemy import select

from db.db import Groups, Product
from settings import session_maker
from loguru import logger



async def get_groups_list() -> list[Groups]:
    logger.info("Запрос на выдачу списка групп из БД")
    session = session_maker()
    group_list = await session.execute(select(Groups))
    return group_list


async def get_group_by_id(id_in: str) -> Groups | None:
    logger.info(f"Запрос на выдачу группы по ID {id_in}")
    session = session_maker()
    groups = await get_groups_list()
    await session.close()
    for group in groups:
        if id_in in group[0].iiko_id:
            return group[0]
    return None


async def get_products_list() -> list[Product]:
    logger.info("Запрос на выдачу списка продуктов")
    session = session_maker()
    product_list = await session.execute(select(Product))
    return product_list


async def get_product_by_id(id_in: str) -> Product | None:
    logger.info(f"Запрос на выдачу продукта по id {id_in}")
    session = session_maker()
    products = await get_products_list()
    await session.close()
    for product in products:
        if id_in == product[0].product_id:
            return product[0]
    return None

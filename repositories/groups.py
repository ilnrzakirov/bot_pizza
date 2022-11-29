from sqlalchemy import select

from db.db import Groups, Product
from settings import session_maker
from loguru import logger

async def get_groups_list() -> list[Groups]:
    logger.info("Запрос на выдачу списка групп из БД")
    session = session_maker()
    group_list = await session.execute(select(Groups))
    await session.close()
    return group_list


async def get_group_by_id(id_in: str, session_in=None) -> Groups | None:
    logger.info(f"Запрос на выдачу группы по ID {id_in}")
    if session_in:
        session = session_in
    else:
        session = session_maker()
    groups = await get_groups_list()
    if session_in is None:
        await session.close()
    for group in groups:
        if id_in in group[0].iiko_id:
            return group[0]
    return None

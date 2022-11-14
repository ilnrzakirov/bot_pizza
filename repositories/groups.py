from sqlalchemy import select

from db.db import Groups
from settings import session_maker


async def get_groups_list() -> list[Groups]:
    session = session_maker()
    group_list = await session.execute(select(Groups))
    return group_list


async def get_group_by_id(id_in: str) -> Groups | None:
    session = session_maker()
    groups = await get_groups_list()
    for group in groups:
        if id_in in group[0].iiko_id:
            return group[0]
    return None

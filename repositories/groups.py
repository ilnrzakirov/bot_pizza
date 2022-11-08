from sqlalchemy import select

from db.db import Groups
from settings import session_maker


async def get_groups_list() -> list[Groups]:
    session = session_maker()
    group_list = await session.execute(select(Groups))
    return group_list

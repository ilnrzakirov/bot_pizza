from decouple import config
from sqlalchemy.engine import URL

from db import (
    asinc_engine,
    get_session_maker,
)

BOT_TOKEN = config("BOT_TOKEN")
postgres_url = URL.create(
    "postgresql+asyncpg",
    username="postgres",
    password="postgres",
    port=5432,
    database="postgres",
    host="localhost",
)

owner = config("OWNER")
API_LOGIN = config("API_LOGIN")
ORG_ID = config("ORG_ID")

async_engine = asinc_engine(postgres_url)
session_maker = get_session_maker(async_engine)  # noqa f841

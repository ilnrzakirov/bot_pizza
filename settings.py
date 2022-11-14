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

groups = {
    "Пицца": "5edeba69-c936-4525-a42e-45372c930b52",
    "Роллы": "309f6cd5-94cd-4430-a943-f8dc2bb371ef e67dade0-0d24-4520-ae82-dbdd8a853d3b 1bca3ac1-6064-408f-ab91-c10b9109ee2c 6a39c5f7-a741-4c25-995a-75fb03d5416c cbc98a12-c83b-4015-8c12-941c00d0cf76",
    "Суши": "9e9ffdf5-1ad2-40b7-bfff-9fb2752feb7d",
    "Паста": "19a79433-e4ec-47b2-807a-c4fa2e1ce16b",
    "Десерты": "892216bc-7907-4b70-92ec-a43ea43060fa",
    "Напитки": "eb75e395-8a45-40a3-8c22-65cc5521f5e6",
    "Салаты": "d9fefd55-9938-4084-9858-4d29223074ad",
    "Закуски": "cac2b8e1-9694-42a1-a503-e2edaa92a125",
    "Комбо": "dc8ff180-f9a3-4ec4-ab20-9d0d9b1c441c",
}
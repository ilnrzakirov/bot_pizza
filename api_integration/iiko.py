import json

import requests
from loguru import logger

from db.db import Groups
from repositories.groups import get_groups_list
from settings import API_LOGIN, ORG_ID, session_maker, groups


async def get_token():
    logger.info("Берем токен АПИ")
    url = "https://api-ru.iiko.services/api/1/access_token"
    body = {
        "apiLogin": API_LOGIN
    }
    try:
        response = requests.post(url=url, json=body)
        data = json.loads(response.text)
        return data["token"]
    except Exception as error:
        logger.error(error)


async def get_menu(token: str):
    logger.info("Запрашиваем меню")
    url = "https://api-ru.iiko.services/api/1/nomenclature"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    body = {
        "organizationId": f"{ORG_ID}"
    }
    try:
        response = requests.post(url=url, headers=headers, json=body)
        data = json.loads(response.text)
        return data
    except Exception as error:
        logger.error(error)


async def set_groups():
    is_set = False
    group_list = await get_groups_list()
    for key, value in groups.items():
        for group in group_list:
            if group[0].name == key:
                is_set = True
                break
        if not is_set:
            session = session_maker()
            new = Groups(name=key, iiko_id=value)
            session.add(new)
            await session.commit()
        is_set = False


import json

import requests
from loguru import logger

from db.db import Groups, Product, Modification
from repositories.groups import get_groups_list, get_group_by_id
from repositories.products import delete_all_products, delete_all_mod, get_product_by_id, get_mod_by_id
from settings import API_LOGIN, ORG_ID, session_maker, groups, URL_IIKO, URL_PROD
from utils.parsing import parsing_json


async def get_token():
    logger.info("Берем токен АПИ")
    url = URL_IIKO
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
    url = URL_PROD
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
    session = session_maker()
    is_set = False
    logger.info("Собираем группы")
    group_list = await get_groups_list()
    for key, value in groups.items():
        for group in group_list:
            if group[0].name == key:
                is_set = True
                break
        if not is_set:
            new = Groups(name=key, iiko_id=value)
            session.add(new)
        is_set = False
    await session.commit()
    await session.close()


async def get_products(data):
    """
        Парсит и записывает в БД продукты
    :param data: json
    :return: None
    """
    logger.info("Собираем продукты")
    market_dict = parsing_json(data)
    session = session_maker()
    product_list = []
    for product in market_dict.get("products_dish"):
        group = await get_group_by_id(product.get("parentGroup"))
        prod = await get_product_by_id(product.get("id"), session)
        if not group:
            continue
        if not prod:
            item = Product(
                product_id=product.get("id"),
                name=product.get("name"),
                group_id=group.id,
                image_url=product.get("imageLinks", "None"),
                description=product.get("description", None),
                price=product.get("sizePrices", 0),
                weight=product.get("weight", 0),
                mod_group=product.get("groupModifiers", None)
            )
            product_list.append(item)
        else:
            prod.name = product.get("name")
            prod.image_url=product.get("imageLinks", "None")
            prod.description=product.get("description", None)
            prod.price=product.get("sizePrices", 0)
            prod.weight=product.get("weight", 0)
            product_list.append(prod)
    session.add_all(product_list)
    await session.commit()
    await session.close()


async def get_modifications(data):
    """
        Парсинг и запсь в БД модификаций
    :param data: json
    :return: None
    """
    logger.info("Собираем модификаторы")
    market_dict = parsing_json(data)
    session = session_maker()
    mod_list = []
    for mod in market_dict.get("products_modifier"):
        modificate = await get_mod_by_id(mod.get("id"), session)
        if not modificate:
            item = Modification(
                mod_id=mod.get("id"),
                name=mod.get("name"),
                price=mod.get("sizePrices", 0),
                weight=mod.get("weight", 0),
                group_id=mod.get("parentGroup", "None"),
                mod_type=mod.get("measureUnit", "None"),
            )
            mod_list.append(item)
        else:
            modificate.name=mod.get("name")
            modificate.price=mod.get("sizePrices", 0)
            modificate.weight=mod.get("weight", 0)
            mod_list.append(modificate)
    session.add_all(mod_list)
    await session.commit()
    await session.close()



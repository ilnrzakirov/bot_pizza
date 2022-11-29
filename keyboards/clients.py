from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.db import Basket, BasketMod, Product, association_prod_basket
from repositories.groups import get_groups_list
from settings import session_maker

delivery = KeyboardButton("🚚 О доставке PizzaHouse")
menu = KeyboardButton("🍽 Меню")
stocks = KeyboardButton("🔥 Акции")
basket = KeyboardButton("🛒 Корзина")
locations = KeyboardButton("📍 Как нас найти")
help = KeyboardButton("⚙ Помощь")
client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
client_keyboard.add(delivery)
client_keyboard.row(menu, stocks)
client_keyboard.add(basket)
client_keyboard.row(locations, help)


async def get_pict(name: str):
    pict_dict = {
    "Пицца": "🍕",
    "Роллы": "🍱",
    "Суши": "🍣",
    "Паста": "🍝",
    "Десерты": "🍰",
    "Напитки": "🥤",
    "Салаты": "🥗",
    "Закуски": "🍟",
    "Комбо": "🥘",
    }
    return pict_dict.get(name, "")


async def get_menu_button():
    groups = await get_groups_list()
    menu_inline = InlineKeyboardMarkup(row_width=2)
    menu_items = []
    for item in groups:
        name = await get_pict(item[0].name)
        name += f" {item[0].name}"
        menu_items.append(InlineKeyboardButton(name, callback_data=f"{item[0].name}"))
    menu_inline.add(*menu_items)
    return menu_inline


async def get_basket(chat_id: str, session_in=None):
    logger.info(f"Запрос на выдачу корзины по id {chat_id}")
    if session_in:
        session = session_in
    else:
        session = session_maker()
    query = select(Basket).where(Basket.chat_id == int(chat_id)).options(selectinload(Basket.products))
    basket = await session.execute(query)
    if session_in is None:
        await session.close()
    return basket.first()

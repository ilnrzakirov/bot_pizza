import aiogram
from aiogram import Dispatcher, types
from aiogram.types import ContentType, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMedia, InputFile, \
    InputMediaPhoto
from aiogram.utils.exceptions import BadRequest
from loguru import logger
from sqlalchemy import select
from sqlalchemy.orm import selectinload

import bot
from db.db import Basket, Product, BasketMod
from keyboards.clients import get_menu_button, get_basket, get_basket_item
from repositories.groups import get_group_by_id
from repositories.modification import get_modifications_by_mod_id
from repositories.products import get_product_by_group_id, get_product_by_iiko_id
from settings import groups, session_maker


async def menu(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username} - id {message.from_user.id}")
    keyboard = await get_menu_button()
    await message.delete()
    await message.answer("🍽  Главное меню", reply_markup=keyboard)


async def delevery(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username} - id {message.from_user.id}")
    await message.answer("Что то есть")


async def stocks(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username} - id {message.from_user.id}")
    await message.answer("Что то есть")


async def basket(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username} - id {message.from_user.id}")
    await message.answer("Что то есть")


async def locations(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username} - id {message.from_user.id}")
    await message.answer("Что то есть")


async def help_menu(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username} - id {message.from_user.id}")
    await message.answer("Что то есть")


async def get_group_items(call: CallbackQuery):
    session = session_maker()
    logger.info(f"Получена команда {call.data} от {call.from_user.username} - id {call.from_user.id}")
    group_name = call.data.split()[0]
    groups_id = groups[group_name]
    group = await get_group_by_id(groups_id, session)
    products = await get_product_by_group_id(group, session)
    keyboard = InlineKeyboardMarkup()
    pos = 0
    if len(call.data.split()) != 1:
        pos = int(call.data.split()[1])
    price = 0
    count = 0
    if basket := await get_basket(call.from_user.id, session):
        logger.info("Корзина получена")
        for prod in basket[0].products:
            items = await get_basket_item(prod.id)
            for product in items:
                count += 1
                price += int(product[0].products[0].price)
    logger.info(f"Состояние корзины count {count}, price {price}")
    add = InlineKeyboardButton("Добавить в корзину", callback_data=f"add {products[pos].product_id}", )
    next = InlineKeyboardButton("➡", callback_data=f"{group_name} {pos + 1}")
    prev = InlineKeyboardButton("⬅", callback_data=f"{group_name} {pos - 1 if pos > 0 else 0}")
    basket_stat = InlineKeyboardButton(f"Корзина: {count} шт. | {price}руб.", callback_data=" ")
    navigate = InlineKeyboardButton(f"{pos + 1}/{len(products)}", callback_data=call.data)
    list_button = InlineKeyboardButton("Списком", callback_data=f"list {group_name}",)
    keyboard.add(add)
    keyboard.row(prev, list_button, next)
    keyboard.add(navigate)
    keyboard.add(basket_stat)
    await session.close()
    file = InputMedia(media=products[pos].image, caption=f"{products[pos].name}\nСостав: {products[pos].description}\n"
                                                         f"Вес: {products[pos].weight}\nЦена: {products[pos].price}")
    try:
        if len(call.data.split()) == 1:
            logger.info("Первый показ карточек товаров")
            await call.message.delete()
            await bot.bot.send_photo(chat_id=call.message.chat.id, photo=products[pos].image, reply_markup=keyboard,
                                     caption=f"{products[pos].name}\nСостав: {products[pos].description}\n"
                                             f"Вес: {products[pos].weight}\nЦена: {products[pos].price}")
        else:
            logger.info("Обновляем карточку товара")
            await call.message.edit_media(media=file, reply_markup=keyboard)
    except BadRequest:
        logger.info("Фото товара не найдеа, подкладываем заглушку")
        file = InputMedia(
            media="https://prikolnye-kartinki.ru/img/picture/Sep/23/9d857169c84422fdaa28df62667a1467/5.jpg",
            caption=f"{products[pos].name}\nСостав: {products[pos].description}\n"
                    f"Вес: {products[pos].weight}\nЦена: {products[pos].price}")
        try:
            await call.message.edit_media(media=file, reply_markup=keyboard)
        except aiogram.utils.exceptions.MessageToEditNotFound:
            logger.info("Нечего редактировать")
            url = "https://prikolnye-kartinki.ru/img/picture/Sep/23/9d857169c84422fdaa28df62667a1467/5.jpg"
            await bot.bot.send_photo(chat_id=call.message.chat.id, photo=url, reply_markup=keyboard,
                                     caption=f"{products[pos].name}\nСостав: {products[pos].description}\n"
                                             f"Вес: {products[pos].weight}\nЦена: {products[pos].price}",
                                     )


async def add_basket(call: CallbackQuery):
    session = session_maker()
    product_id = call.data.split()[1]
    product = await get_product_by_iiko_id(product_id, session)
    mod_id = product.mod_group
    data = await get_modifications_by_mod_id(mod_id, session)
    if basket := await get_basket(call.from_user.id, session):
        logger.info("Корзина получена")
    else:
        basket = Basket(
            chat_id=int(call.from_user.id),
        )
        session.add(basket)
        await session.commit()
    if data:
        mod_keyboard = InlineKeyboardMarkup()
        for item in data:
            text = item.name.replace("; Т", ", Тонкое тесто").replace("; П", ", Пышное тесто")
            text = f"{text} {int(item.price)} руб"
            button = InlineKeyboardButton(text=text, callback_data=f"mod {item.mod_id}")
            mod_keyboard.add(button)
        chat = call.from_user.id
        await call.message.delete()
        await bot.bot.send_message(chat_id=chat, text="Выбери размер", reply_markup=mod_keyboard)
    else:
        basket_prod = BasketMod(
            products=[product]
        )
        basket[0].products.append(basket_prod)
        session.add(basket_prod)
        await session.commit()
        await session.close()
        await call.message.answer("Добавлен в корзину")


async def list_view(call: CallbackQuery):
    """
        Покаывает список товаров определенной группы в виде списка
    :param call: CallbackQuery (id группы)
    :return: None
    """
    group_name = call.data.split()[1]
    groups_id = groups[group_name]
    group = await get_group_by_id(groups_id)
    products = await get_product_by_group_id(group)
    keyboard = InlineKeyboardMarkup(row_width=2)
    items_list = []
    pos = 0
    for item in products:
        items_list.append(InlineKeyboardButton(item.name, callback_data=f"view {group_name} {pos}"))
        pos += 1
    keyboard.add(*items_list)
    await call.message.delete()
    await call.message.answer("Выбери: ", reply_markup=keyboard)


async def detail_view(call: CallbackQuery):
    """
        Показ карточки товара при выборе со списка товаров
    :param call: CallbackQuery
    :return: None
    """
    group_name = call.data.split()[1]
    pos = int(call.data.split()[2])
    groups_id = groups[group_name]
    group = await get_group_by_id(groups_id)
    products = await get_product_by_group_id(group)
    add = InlineKeyboardButton("Добавить в корзину", callback_data=f"add {products[pos].product_id}", )
    next = InlineKeyboardButton("➡", callback_data=f"{group_name} {pos + 1}")
    prev = InlineKeyboardButton("⬅", callback_data=f"{group_name} {pos - 1 if pos > 0 else 0}")
    navigate = InlineKeyboardButton(f"{pos + 1}/{len(products)}", callback_data=call.data)
    list_button = InlineKeyboardButton("Списком", callback_data=f"list {group_name}")
    keyboard = InlineKeyboardMarkup()
    keyboard.add(add)
    keyboard.row(prev, list_button, next)
    keyboard.add(navigate)
    file = InputMedia(media=products[pos].image, caption=f"{products[pos].name}\nСостав: {products[pos].description}\n"
                                                         f"Вес: {products[pos].weight}\nЦена: {products[pos].price}")

    await call.message.delete()
    await bot.bot.send_photo(chat_id=call.message.chat.id, photo=products[pos].image, reply_markup=keyboard,
                             caption=f"{products[pos].name}\nСостав: {products[pos].description}\n"
                                     f"Вес: {products[pos].weight}\nЦена: {products[pos].price}")


def register_handlers_client(dispatcher: Dispatcher):
    dispatcher.register_message_handler(menu, text="🍽 Меню", content_types=ContentType.TEXT)
    dispatcher.register_message_handler(delevery, text="🚚 О доставке PizzaHouse", content_types=ContentType.TEXT)
    dispatcher.register_message_handler(stocks, text="🔥 Акции", content_types=ContentType.TEXT)
    dispatcher.register_message_handler(basket, text="🛒 Корзина", content_types=ContentType.TEXT)
    dispatcher.register_message_handler(locations, text="📍 Как нас найти", content_types=ContentType.TEXT)
    dispatcher.register_message_handler(help_menu, text="⚙ Помощь", content_types=ContentType.TEXT)
    dispatcher.register_callback_query_handler(get_group_items, lambda call: call.data.split(" ")[0] in groups.keys(), )
    dispatcher.register_callback_query_handler(add_basket, lambda call: call.data.startswith("add"), )
    dispatcher.register_callback_query_handler(list_view, lambda call: call.data.startswith("list"), )
    dispatcher.register_callback_query_handler(detail_view, lambda call: call.data.startswith("view"), )

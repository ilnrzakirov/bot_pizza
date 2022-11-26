import aiogram
from aiogram import Dispatcher, types
from aiogram.types import ContentType, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputMedia, InputFile, \
    InputMediaPhoto
from aiogram.utils.exceptions import BadRequest
from loguru import logger

import bot
from keyboards.clients import get_menu_button
from repositories.groups import get_group_by_id
from repositories.modification import get_modifications_by_mod_id
from repositories.products import get_product_by_group_id, get_product_by_iiko_id
from settings import groups


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
    logger.info(f"Получена команда {call.data} от {call.from_user.username} - id {call.from_user.id}")
    group_name = call.data.split()[0]
    groups_id = groups[group_name]
    group = await get_group_by_id(groups_id)
    products = await get_product_by_group_id(group)
    keyboard = InlineKeyboardMarkup()
    pos = 0
    if len(call.data.split()) != 1:
        pos = int(call.data.split()[1])
    add = InlineKeyboardButton("Добавить в корзину", callback_data=f"add {products[pos].product_id}",)
    next = InlineKeyboardButton("➡", callback_data=f"{group_name} {pos + 1}")
    prev = InlineKeyboardButton("⬅", callback_data=f"{group_name} {pos - 1 if pos > 0 else 0}")
    navigate = InlineKeyboardButton(f"{pos + 1}/{len(products)}", callback_data=call.data)
    keyboard.add(add)
    keyboard.row(prev, next)
    keyboard.add(navigate)
    file = InputMedia(media=products[pos].image, caption=f"{products[pos].name}\nСостав: {products[pos].description}\n"
                                                   f"Вес: {products[pos].weight}\nЦена: {products[pos].price}")
    try:
        if len(call.data.split()) == 1:
            await call.message.delete()
            await bot.bot.send_photo(chat_id=call.message.chat.id, photo=products[pos].image, reply_markup=keyboard,
                                     caption=f"{products[pos].name}\nСостав: {products[pos].description}\n"
                                             f"Вес: {products[pos].weight}\nЦена: {products[pos].price}")
        else:
            await call.message.edit_media(media=file, reply_markup=keyboard)
    except BadRequest:
        file = InputMedia(media="https://prikolnye-kartinki.ru/img/picture/Sep/23/9d857169c84422fdaa28df62667a1467/5.jpg",
                          caption=f"{products[pos].name}\nСостав: {products[pos].description}\n"
                                               f"Вес: {products[pos].weight}\nЦена: {products[pos].price}")
        await call.message.edit_media(media=file, reply_markup=keyboard)


async def add_basket(call: CallbackQuery):
    product_id = call.data.split()[1]
    product = await get_product_by_iiko_id(product_id)
    mod_id = product.mod_group
    data = await get_modifications_by_mod_id(mod_id)
    if data:
        mod_keyboard = InlineKeyboardMarkup()
        for item in data:
            text = item.name.replace("; Т", ", Тонкое тесто").replace("; П", ", Пышное тесто")
            text = f"{text} {int(item.price)} руб"
            button = InlineKeyboardButton(text=text, callback_data=f"{item.mod_id}")
            mod_keyboard.add(button)
        chat = call.from_user.id
        await call.message.delete()
        await bot.bot.send_message(chat_id=chat, text="Выбери размер", reply_markup=mod_keyboard)
    else:
        await call.message.answer("Добавлен в корзину")


def register_handlers_client(dispatcher: Dispatcher):
    dispatcher.register_message_handler(menu, text="🍽 Меню", content_types=ContentType.TEXT)
    dispatcher.register_message_handler(delevery, text="🚚 О доставке PizzaHouse", content_types=ContentType.TEXT)
    dispatcher.register_message_handler(stocks, text="🔥 Акции", content_types=ContentType.TEXT)
    dispatcher.register_message_handler(basket, text="🛒 Корзина", content_types=ContentType.TEXT)
    dispatcher.register_message_handler(locations, text="📍 Как нас найти", content_types=ContentType.TEXT)
    dispatcher.register_message_handler(help_menu, text="⚙ Помощь", content_types=ContentType.TEXT)
    dispatcher.register_callback_query_handler(get_group_items, lambda call: call.data.split(" ")[0] in groups.keys(),)
    dispatcher.register_callback_query_handler(add_basket, lambda call: call.data.startswith("add"),)


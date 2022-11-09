from aiogram import Dispatcher, types
from aiogram.types import ContentType, CallbackQuery
from loguru import logger

from keyboards.clients import get_menu_button
from settings import groups


async def menu(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username} - id {message.from_user.id}")
    keyboard = await get_menu_button()
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
    await call.message.answer(text="Ok")

def register_handlers_client(dispatcher: Dispatcher):
    dispatcher.register_message_handler(menu, text="🍽 Меню", content_types=ContentType.TEXT)
    dispatcher.register_message_handler(delevery, text="🚚 О доставке PizzaHouse", content_types=ContentType.TEXT)
    dispatcher.register_message_handler(stocks, text="🔥 Акции", content_types=ContentType.TEXT)
    dispatcher.register_message_handler(basket, text="🛒 Корзина", content_types=ContentType.TEXT)
    dispatcher.register_message_handler(locations, text="📍 Как нас найти", content_types=ContentType.TEXT)
    dispatcher.register_message_handler(help_menu, text="⚙ Помощь", content_types=ContentType.TEXT)
    dispatcher.register_callback_query_handler(get_group_items, lambda call: call.data in groups.keys(),)

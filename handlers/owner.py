from aiogram import Dispatcher, types
from aiogram.types import ContentType

from api_integration.iiko import get_token, get_menu, set_groups, get_products, get_modifications


async def update_menu(message: types.Message):
    token = await get_token()
    data = await get_menu(token)
    await set_groups()
    await get_products(data)


def register_handlers_owner(dispatcher: Dispatcher):
    dispatcher.register_message_handler(update_menu, text="update", content_types=ContentType.TEXT)

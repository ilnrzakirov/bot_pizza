from aiogram import Dispatcher, types
from aiogram.types import ContentType

from api_integration.iiko import get_token, get_menu


async def update_menu(message: types.Message):
    token = await get_token()
    data = await get_menu(token)


def register_handlers_owner(dispatcher: Dispatcher):
    dispatcher.register_message_handler(update_menu, text="update", content_types=ContentType.TEXT)

from aiogram import types, Dispatcher
from loguru import logger

from keyboards.owner import owner_keyboard
from settings import owner


async def start(message: types.Message):
    logger.info(f"Получена команда {message.text} от {message.from_user.username} - id {message.from_user.id}")
    if message.from_user.id == int(owner):
        return await message.answer("Привет", reply_markup=owner_keyboard)


def register_handlers(dispatcher: Dispatcher):
    """
        Функция для регистрации хендлеров
    :param dispatcher: Dispatcher
    :return: Хендлер
    """
    dispatcher.register_message_handler(start, commands=["start"])

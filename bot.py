import asyncio

from aiogram.utils import executor  # noqa F401

from bot_init import (
    bot,
    dispatcher,
)
from handlers import start, client
from utils.loger_init import logger
from handlers import owner


@logger.catch()
async def on_startup(_):
    logger.info("Бот запущен")


@logger.catch()
async def main():
    start.register_handlers(dispatcher)
    owner.register_handlers_owner(dispatcher)
    client.register_handlers_client(dispatcher)
    logger.info("Бот запущен")
    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as error:
        logger.error(error)

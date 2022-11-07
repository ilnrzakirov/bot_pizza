from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

update_menu = KeyboardButton("update")

owner_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
owner_keyboard.add(update_menu)

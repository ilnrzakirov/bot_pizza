from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

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


async def get_menu_button():
    groups = [] # TODO вытащить с бд
    menu_inline = InlineKeyboardMarkup()
    for item in groups:
        menu_inline.add(InlineKeyboardButton(f"{item.name}", callback_data=f"{item.iiko_id}"))
    return menu_inline

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu_keyboard():
    buttons = [
        [KeyboardButton(text="📦 Каталог")],
        [KeyboardButton(text="🔍 Наличие товара"), KeyboardButton(text="🔒 Бронирование")],
        [KeyboardButton(text="⭐ Моя лояльность"), KeyboardButton(text="🎁 Акции")],
        [KeyboardButton(text="📍 Адрес и часы"), KeyboardButton(text="💬 Связь с продавцом")],
        [KeyboardButton(text="❓ FAQ"), KeyboardButton(text="📜 История покупок")],
        [KeyboardButton(text="📱 О боте / Функции")]   # новая кнопка
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def categories_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🐾 Корм", callback_data="cat_Корм")],
        [InlineKeyboardButton(text="🧴 Гигиена", callback_data="cat_Гигиена")],
        [InlineKeyboardButton(text="🎾 Игрушки", callback_data="cat_Игрушки")],
        [InlineKeyboardButton(text="◀ Назад", callback_data="main_menu")]
    ])
    return kb

def products_keyboard(products):
    buttons = []
    for p in products:
        buttons.append([InlineKeyboardButton(text=f"{p[1]} — {p[2]}₽ (в наличии: {p[3]})", callback_data=f"product_{p[0]}")])
    buttons.append([InlineKeyboardButton(text="◀ Назад к категориям", callback_data="back_categories")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def product_detail_keyboard(product_id, in_stock):
    kb = []
    if in_stock:
        kb.append([InlineKeyboardButton(text="🔒 Забронировать", callback_data=f"book_{product_id}")])
    kb.append([InlineKeyboardButton(text="◀ Назад", callback_data="back_to_products")])
    return InlineKeyboardMarkup(inline_keyboard=kb)

def booking_confirm_keyboard(booking_id, product_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Подтверждаю покупку", callback_data=f"confirm_purchase_{booking_id}_{product_id}")],
        [InlineKeyboardButton(text="❌ Отменить бронь", callback_data=f"cancel_booking_{booking_id}")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")]
    ])
    return kb

def inline_map_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗺 Открыть карту", callback_data="map_open")]
    ])

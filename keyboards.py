from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from database import get_all_categories, get_products_by_category, get_cart_products_for_delete, get_user_info


def generate_phone_button():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='Send your contact', request_contact=True)]
    ], resize_keyboard=True)


def generate_location_button(chat_id):
    user_info = get_user_info(chat_id)
    location = user_info[0][2]
    if location:
        return ReplyKeyboardMarkup([
            [KeyboardButton(text='Send your location', request_location=True)],
            [KeyboardButton(text=f'📍 {location}')]
        ], resize_keyboard=True)
    else:
        return ReplyKeyboardMarkup([
            [KeyboardButton(text='Send your location', request_location=True)]
        ], resize_keyboard=True)


def choice():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='✅ Yes'), KeyboardButton(text='❌ No')]
    ], resize_keyboard=True)


def generate_main_menu():
    return ReplyKeyboardMarkup([
        [KeyboardButton(text='✔️ Make an order')],
        [KeyboardButton(text='🗒️️️ My orders'), KeyboardButton(text='🛒 Cart'), KeyboardButton(text='⚙️ Settings')]
    ])


def generate_settings_options(chat_id):
    user_info = get_user_info(chat_id)
    full_name = user_info[0][0]
    phone = user_info[0][1]
    return ReplyKeyboardMarkup([
        [KeyboardButton(text=f'Edit name ({full_name})')],
        [KeyboardButton(text=f'Edit number ({phone})')],
        [KeyboardButton(text='⬅️ Back')]
    ])


def generate_category_menu():
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text='🍴 Menu', url='https://telegra.ph/Menu-03-05-3')
    )
    categories = get_all_categories()
    buttons = []
    for category in categories:
        btn = InlineKeyboardButton(text=category[1], callback_data=f'category_{category[0]}')
        buttons.append(btn)
    markup.add(*buttons)
    return markup


def generate_products_by_category(category_id):
    markup = InlineKeyboardMarkup(row_width=2)
    products = get_products_by_category(category_id)
    buttons = []
    for product in products:
        btn = InlineKeyboardButton(text=product[1], callback_data=f'product_{product[0]}')
        buttons.append(btn)
    markup.add(*buttons)
    markup.row(
        InlineKeyboardButton(text='⬅️ Back', callback_data='main_menu')
    )
    return markup


def generate_product_detail_menu(product_id, category_id):
    markup = InlineKeyboardMarkup(row_width=3)
    numbers = [i for i in range(1, 10)]
    buttons = []
    for number in numbers:
        btn = InlineKeyboardButton(text=str(number), callback_data=f'cart_{product_id}_{number}')
        buttons.append(btn)
    markup.add(*buttons)
    markup.row(
        InlineKeyboardButton(text='⬅️ Back', callback_data=f'back_{category_id}')
    )
    return markup


def generate_cart_menu(cart_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.row(
        InlineKeyboardButton(text='🚀 Make an order', callback_data=f'order_{cart_id}')
    )
    cart_products = get_cart_products_for_delete(cart_id)
    buttons = []
    for cart_product_id, product_name in cart_products:
        btn = InlineKeyboardButton(text=f'❌ {product_name}', callback_data=f'delete_{cart_product_id}')
        buttons.append(btn)
    markup.add(*buttons)
    return markup

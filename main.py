from aiogram import Dispatcher, Bot, executor
from aiogram.types import Message, CallbackQuery, LabeledPrice
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards import *
from database import *
from location import *
from order_number import *
from dotenv import load_dotenv
import os

load_dotenv()

storage = MemoryStorage()
TOKEN = os.getenv('TOKEN')
PAYME = os.getenv('PAYMENT')
bot = Bot(TOKEN, parse_mode='HTML')
dp = Dispatcher(bot=bot, storage=storage)

order_num = 0


class UserUpdate(StatesGroup):
    name = State()
    phone = State()
    location = State()


@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    await message.answer(f'Hello\nWelcome to delivery bot')
    await register_user(message)


async def register_user(message: Message):
    chat_id = message.chat.id
    full_name = message.from_user.first_name
    user = first_select_user(chat_id)
    if user:
        await message.answer('Authorization has been completed successfully')
        await show_main_menu(message)
    else:
        first_register_user(chat_id, full_name)
        await message.answer('For registration click on the button', reply_markup=generate_phone_button())


@dp.message_handler(content_types=['contact'])
async def continue_register(message: Message):
    chat_id = message.chat.id
    phone = message.contact.phone_number
    update_user_to_finish_register(chat_id, phone)
    await create_cart_for_user(message)
    await show_main_menu(message)


async def create_cart_for_user(message: Message):
    chat_id = message.chat.id
    try:
        insert_to_cart(chat_id)
    except:
        pass


async def show_main_menu(message: Message):
    await message.answer('Select from the following', reply_markup=generate_main_menu())


@dp.message_handler(lambda message: '✔️ Make an order' in message.text)
# @dp.message_handler(regexp='✔️ Make an order')
async def make_order(message: Message):
    chat_id = message.chat.id
    await message.answer('Click on the button to send your location or select from suggested ones', reply_markup=generate_location_button(chat_id))


@dp.message_handler(content_types=['location'])
async def get_user_location(message: Message):
    chat_id = message.chat.id
    location = message.location
    user_location = get_location(chat_id, location)
    await message.answer(f'Address where you want to order:\n<b>{user_location}</b>\nDo you verify this address?', reply_markup=choice())


@dp.message_handler(regexp='✅ Yes')
async def right_location(message: Message):
    await message.answer(text='Your location has been saved successfully', reply_markup=generate_main_menu())
    await begin_menu(message)


@dp.message_handler(regexp='❌ No')
async def wrong_location(message: Message):
    await make_order(message)


async def begin_menu(message: Message):
    await message.answer('Choose the category', reply_markup=generate_category_menu())


@dp.message_handler(regexp='⚙️ Settings')
async def show_settings_options(message: Message):
    chat_id = message.chat.id
    await message.answer('Choose from the following', reply_markup=generate_settings_options(chat_id))


@dp.callback_query_handler(lambda call: 'category' in call.data)
async def show_products(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, category_id = call.data.split('_')
    category_id = int(category_id)
    await bot.edit_message_text('Choose product', chat_id, message_id,
                                reply_markup=generate_products_by_category(category_id))


@dp.callback_query_handler(lambda call: 'main_menu' in call.data)
async def return_to_main_menu(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    await bot.edit_message_text(chat_id=chat_id,
                                message_id=message_id,
                                text='Choose category',
                                reply_markup=generate_category_menu())


@dp.callback_query_handler(lambda call: 'product' in call.data)
async def show_detail_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, product_id = call.data.split('_')
    product_id = int(product_id)
    product = get_product_detail(product_id)
    await bot.delete_message(chat_id, message_id)
    with open(product[-1], mode='rb') as img:
        await bot.send_photo(chat_id=chat_id,
                             photo=img,
                             caption=f'''{product[2]}
Price: {product[-3]} sum
Description: {product[-2]}
Choose or enter quantity''', reply_markup=generate_product_detail_menu(product_id=product_id, category_id=product[1]))


@dp.callback_query_handler(lambda call: 'back' in call.data)
async def return_to_category(call: CallbackQuery):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    _, category_id = call.data.split('_')
    await bot.delete_message(chat_id, message_id)
    await bot.send_message(chat_id, 'Choose category', reply_markup=generate_products_by_category(category_id))


@dp.callback_query_handler(lambda call: call.data.startswith('cart'))
async def add_product_cart(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, product_id, quantity = call.data.split('_')
    product_id, quantity = int(product_id), int(quantity)
    cart_id = get_user_cart_id(chat_id)
    product = get_product_detail(product_id)
    final_price = product[3] * quantity

    if insert_or_update_cart_product(cart_id, product[2], quantity, final_price):
        await bot.answer_callback_query(call.id, 'Product has been added successfully')
    else:
        await bot.answer_callback_query(call.id, 'Quantity has been changed successfully')


@dp.message_handler(regexp=r'🛒 Cart')
async def show_cart(message: Message, edit_message: bool = False):
    chat_id = message.chat.id
    cart_id = get_user_cart_id(chat_id)
    try:
        update_total_products_total_price(cart_id)
    except Exception as e:
        print(e)
        await message.answer("Cart isn't available\nContact the Support Center")
        return

    total_products, total_price = get_total_products_price(cart_id)
    # print(total_products, total_price)
    cart_products = get_cart_products(cart_id)
    text = '🛒 Cart:\n\n'
    for product_name, quantity, final_price in cart_products:
        text += f'''<b>{product_name}</b>
{quantity} ✖ {int(final_price / quantity)} = {final_price} som\n\n'''
    text += f'''Total quantity of products:  {0 if total_products is None else total_products}
Total:  {0 if total_price is None else total_price} som'''

    if edit_message:
        await bot.edit_message_text(text, chat_id, message.message_id, reply_markup=generate_cart_menu(cart_id))
    else:
        await bot.send_message(chat_id, text, reply_markup=generate_cart_menu(cart_id))


@dp.callback_query_handler(lambda call: 'delete' in call.data)
async def delete_cart_product(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, cart_product_id = call.data.split('_')
    message = call.message
    cart_product_id = int(cart_product_id)
    delete_cart_product_from_database(cart_product_id)
    await bot.answer_callback_query(call.id, text='Product has been deleted successfully')
    await show_cart(message, edit_message=True)


@dp.callback_query_handler(lambda call: 'order' in call.data)
async def create_order(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, cart_id = call.data.split('_')
    cart_id = int(cart_id)

    total_products, total_price = get_total_products_price(cart_id)
    user_info = get_user_info(chat_id)
    user_location = user_info[0][2]
    # print(total_products, total_price)
    cart_products = get_cart_products(cart_id)
    text = '🛒 Cart:\n\n'
    for product_name, quantity, final_price in cart_products:
        text += f'''{product_name}
{quantity} ✖ {int(final_price / quantity)} = {final_price} som\n\n'''
    text += f'''\nTotal quantity of products:  {0 if total_products is None else total_products}
\nTotal:  {0 if total_price is None else total_price} som
\nDelivery: 10000 som
\nLocation: {user_location}'''

    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    INSERT INTO history(telegram_id, history) VALUES (?, ?)
    ''', (chat_id, str(text)))
    database.commit()
    database.close()
    global order_num
    order_number(order_num)
    order_num += 1
    await bot.send_invoice(
        chat_id=chat_id,
        title=f'Order №{order_num}',
        description=text,
        payload='bot-defined invoice payload',
        provider_token=PAYME,
        currency='UZS',
        prices=[
            LabeledPrice(label='Total', amount=int(total_price * 100)),
            LabeledPrice(label='Delivery', amount=1000000)
        ]
    )

    await bot.send_message(chat_id, 'The order has been paid successfully')
    clear_cart(cart_id)


@dp.message_handler(regexp='⬅️ Back')
async def back_to_menu(message: Message):
    await message.answer('Choose from the following', reply_markup=generate_main_menu())


@dp.message_handler(regexp='Edit name')
async def ask_name(message: Message):
    await message.answer('Enter your new name', reply_markup=ReplyKeyboardRemove())
    await UserUpdate.name.set()


@dp.message_handler(state=UserUpdate.name)
async def edit_name(message: Message, state: FSMContext):
    if message.text in ['/start']:
        await show_main_menu(message)
    else:
        chat_id = message.chat.id
        new_name = message.text
        edit_user_name(chat_id, new_name)
        await message.answer('The name has changed successfully', reply_markup=generate_settings_options(chat_id))
        await state.finish()


@dp.message_handler(regexp='Edit number')
async def ask_number(message: Message):
    await message.answer('Enter your new phone number', reply_markup=ReplyKeyboardRemove())
    await UserUpdate.phone.set()


@dp.message_handler(state=UserUpdate.phone)
async def edit_number(message: Message, state: FSMContext):
    if message.text in ['/start']:
        await show_main_menu(message)
    else:
        chat_id = message.chat.id
        new_phone = message.text
        edit_user_phone(chat_id, new_phone)
        await message.answer('The phone number has changed successfully', reply_markup=generate_settings_options(chat_id))
        await state.finish()


@dp.message_handler(regexp='🗒️️️ My orders')
async def get_history(message: Message):
    chat_id = message.chat.id
    database = sqlite3.connect('fastfood.db')
    cursor = database.cursor()
    cursor.execute('''
    SELECT history FROM history
    WHERE telegram_id = ?;
    ''', (chat_id, ))
    history = cursor.fetchall()
    database.commit()
    database.close()
    history = history[::-1]
    if history:
        for h in history[:5]:
            await bot.send_message(chat_id, f'{history[0][0]}')
    else:
        await bot.send_message(chat_id, 'You haven\'t ordered anything yet')


@dp.message_handler(regexp='📍')
async def previous_location(message: Message):
    chat_id = message.chat.id
    location = message.text[2::]
    update_user_to_finish_register2(chat_id, location)
    await message.answer('Your location has been saved successfully', reply_markup=generate_main_menu())
    await begin_menu(message)


executor.start_polling(dp)

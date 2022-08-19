from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from config import ADMIN
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import bot

class FSMAdmin(StatesGroup):  # Finite State Machine
    photo = State()
    title = State()
    description = State()
    price = State()

async def fsm_start(message: types.Message):
    if message.from_user.id in ADMIN:
        await FSMAdmin.photo.set()
        await message.answer(f"Привет {message.from_user.full_name} "
                             f"Отправьте фото блюда.")
    else:
        await message.reply("Пишите строго в личку!")

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as menu:
        menu['id'] = message.from_user.id
        menu['username'] = f"@{message.from_user.username}"
        menu['photo'] = message.photo[0].file_id
    await FSMAdmin.next()
    await message.answer("Введите название блюда.")

async def load_title(message: types.Message, state: FSMContext):
    async with state.proxy() as menu:
        menu['title'] = message.text
    await FSMAdmin.next()
    await message.answer('Опишите ваше блюдо.')

async def load_description(message: types.Message, state: FSMContext):
    async with state.proxy() as menu:
        menu['description'] = message.text
    await FSMAdmin.next()
    await message.answer('Цена вашего блюда.')

async def load_price(message: types.Message, state: FSMContext):
    try:
        if int(message.text) < 100000:
            async with state.proxy() as menu:
                menu['price'] = float(message.text)
                await bot.send_photo(message.from_user.id, menu['photo'],
                                     caption=f"Title: {menu['title']}\n"
                                             f"description: {menu['description']}\n"
                                             f"Price: {menu['price']}\n\n"
                                             f"{menu['username']}")
        else:
            await bot.send_message(message.chat.id, 'Да...Дада...')
    except:
        await bot.send_message('Вводите строго цифры!')

    await state.finish()
    await message.answer("Интересное блюдо")

def register_handlers_fsmAdminmenu(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=['menu'])
    dp.register_message_handler(load_photo, state=FSMAdmin.photo,
                                content_types=['photo'])
    dp.register_message_handler(load_title, state=FSMAdmin.title)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
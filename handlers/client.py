from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot, Dispatcher
import random
import time
async def start(message: types.Message):
    await bot.send_message(message.chat.id, 'commands: /mem, /quiz, /dice (if u admin game), !pin with reply message')
async def pin(message: types.Message):
    await bot.pin_chat_message(message.chat.id, message.reply_to_message.message_id)
async def dice(message: types.Message):
    if message.chat.type != "private":
        await bot.send_message(message.chat.id, 'For bot:')
        bot_choice = await bot.send_dice(message.chat.id, emoji='🎲')
        await bot.send_message(message.chat.id, 'For player:')
        player_choice = await bot.send_dice(message.chat.id, emoji='🎲')
        time.sleep(5)
        print(bot_choice.dice.value)
        print(player_choice.dice.value)
        if bot_choice.dice.value > player_choice.dice.value:
            await bot.send_message(message.chat.id, 'Победа за мной. Бот оказался лучше игрока.')
        elif bot_choice.dice.value == player_choice.dice.value:
            await bot.send_message(message.chat.id, 'Ничья,но я ещё отыграюсь')
        else:
            await bot.send_message(message.chat.id, 'Игрок выиграл. Ему повезло,в следующий раз такого не случится')
    else:
        await message.reply('пиши только в группе')
async def meme(message: types.message):
    image = ['media/1.png' ,'media/2.jpg','media/b.jpg','media/da.jpg','media/eh.jpg', 'media/fact.jpg', \
             'media/image1-drake-posting-meme.jpg', 'media/jiza.jpg', 'media/jizaa.jpg','media/laba.jpg', \
             'media/lool.jpg']
    photo = open(random.choice(image), 'rb')
    await bot.send_photo(message.chat.id, photo=photo)
async def quiz1(message: types.Message):
    markup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton("NEXT", callback_data='button_call_1')
    markup.add(button_call_1)
    question = "Кто создал Python?"
    answers = [
        "Гвидо Ван Россум",
        "Брутал Мэн",
        "Умный чел",
        "Я не знаю",
        "Майкл Джордан"
    ]
    await bot.send_poll(
        chat_id=message.chat.id,
        question=question,
        options=answers,
        is_anonymous=False,
        type='quiz',
        correct_option_id=0,
        open_period=10,
        explanation="Лол,ладно,это же очевидно",
        reply_markup=markup
    )
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(meme, commands=['mem'])
    dp.register_message_handler(quiz1, commands=['quiz'])
    dp.register_message_handler(pin, commands=['pin'], commands_prefix='!')
    dp.register_message_handler(dice, commands=['dice'])
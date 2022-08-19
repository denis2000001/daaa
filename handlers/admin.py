from aiogram import types, Dispatcher
from config import bot
from config import ADMIN
import random
async def game(message: types.Message):
    games = ['🎯', '🎳', '🎲', '🎰', '🏀', '⚽️']
    r_games = random.choice(games)
    if message.text.startswith('game'):
        if message.chat.type != "private":
            if message.from_id in ADMIN:
                await bot.send_dice(message.chat.id, emoji=r_games)
            else:
                await message.reply('Ой бой,ты мне не босс!')
        else:
            await message.reply('пиши только в группе бигбрейн')
def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(game)
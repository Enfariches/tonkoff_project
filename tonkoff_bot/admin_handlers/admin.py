from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import dp, logger, ADMIN_USER_ID
from wallet_handlers.wallet_state import *

from database.db_bot import create_message

@dp.message(Command("send"))
async def broadcast_message(message: Message, state: FSMContext):
    
    try:
        if message.from_user.id in ADMIN_USER_ID:
            await message.reply("Пришлите текст для рассылки")
            await create_message(user_username=message.from_user.username)
            await state.set_state(WalletState.waiting_for_text)
        else:
            await message.reply("Вы не админ")
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователь: {message.from_user.username} ({message.from_user.id})")
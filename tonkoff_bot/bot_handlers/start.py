from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from aiogram.utils.deep_linking import decode_payload

from config import dp, bot, logger
import board as b

from database.db_bot import create_profile, create_check_user
from sqlalchemy.ext.asyncio import AsyncSession

@dp.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
     
    try:
        args = message.text.split(' ')[1]
        payload = int(decode_payload(args))
    except Exception as e:
        payload = None
    
    try:
        await create_profile(session, message.from_user.id, message.from_user.username, payload)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {message.from_user.username} ({message.from_user.id})")
    
    try:
        await create_check_user(session, message.from_user.id)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {message.from_user.username} ({message.from_user.id})")

    greeting_message = (f"Салют, {message.from_user.username}, вот и настало твое время становиться миллионером!✈️ \n"
                        f"Начни свой путь правильно:\n"
                        f"· Присоединяйся к нашему каналу @aleg_tonkoff\n"
                        f"· Разомни свои пальчики в кликере и заработай немного деньжат\n"
                        f"· Приглашай бизнес-партнеров \n"
                        f"Осмотрись тут, потягивая джин-тоник")
    await bot.send_photo(chat_id=message.from_user.id, photo=FSInputFile(path="tonkoff_bot/assets/start_picture.jpg"), caption=greeting_message, reply_markup=b.start_board)
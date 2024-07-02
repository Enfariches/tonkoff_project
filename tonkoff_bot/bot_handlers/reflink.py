from aiogram.types import CallbackQuery, FSInputFile
from aiogram.utils.deep_linking import create_start_link
from aiogram import F

from config import dp, bot, logger
import board as b

from database.db_bot import update_link_profile
from sqlalchemy.ext.asyncio import AsyncSession


@dp.callback_query(F.data == "Рефка")
async def query_handler(callback_query: CallbackQuery, session: AsyncSession):
    
    link = await create_start_link(bot=bot, payload=str(callback_query.from_user.id), encode=True)

    try:
        await update_link_profile(session, callback_query.from_user.id, link)
        await bot.send_photo(chat_id=callback_query.from_user.id, photo=FSInputFile(path="tonkoff_bot/assets/ref_picture.jpg"), 
                            caption=f"Твоя ссылка для приглашения партнеров: {link}\n\nТы будешь получать 30% от всех их $Tonkoff points!📈",
                            reply_markup=b.menu_board)
        await callback_query.message.delete()
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователь: {callback_query.from_user.username} ({callback_query.from_user.id})")
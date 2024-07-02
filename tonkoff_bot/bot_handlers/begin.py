from aiogram.types import CallbackQuery, FSInputFile
from aiogram import F

from config import dp, bot, logger
import board as b

from database.db_bot import update_check
from sqlalchemy.ext.asyncio import AsyncSession

@dp.callback_query(F.data == "Начать")
async def query_handler(callback_query: CallbackQuery, session: AsyncSession):

    user_channel_status_ru = await bot.get_chat_member(chat_id='@myfavhero', user_id=callback_query.from_user.id)
    if user_channel_status_ru.status != "left":
        
        try:
            await update_check(session, callback_query.from_user.id, "canal_ru")
            await bot.send_photo(chat_id=callback_query.from_user.id,
                                    photo=FSInputFile(path="tonkoff_bot/assets/status_picture.jpg"),
                                    reply_markup=b.menu_board)
            await callback_query.message.delete()
        except Exception as e:
            logger.error(f"Ошибка: {e}. Пользователя: {callback_query.from_user.username} ({callback_query.from_user.id})")
    else:
        await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Вы не подписались на канал https://t.me/aleg_tonkoff', show_alert=True)
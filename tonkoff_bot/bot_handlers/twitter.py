from aiogram.types import CallbackQuery
from aiogram import F

from config import dp, bot, logger
import board as b

from database.db_bot import update_balance, status_check, update_check
from sqlalchemy.ext.asyncio import AsyncSession

@dp.callback_query(F.data == "Twitter")
async def query_handler(callback_query: CallbackQuery):

    await bot.send_message(chat_id=callback_query.from_user.id, text="Follow the news!", reply_markup=b.twitter_board)
    await callback_query.message.delete()

@dp.callback_query(F.data == "Проверка_twitter")
async def query_handler(callback_query: CallbackQuery, session: AsyncSession):

    try:
        already_checked = await status_check(session, callback_query.from_user.id, "quest_1")
        if already_checked:
            await bot.answer_callback_query(callback_query_id=callback_query.id,
                                            text='You have already received points for subscribing', show_alert=True)
            return
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователь: {callback_query.from_user.username} ({callback_query.from_user.id})")

    try:
        await update_check(session, callback_query.from_user.id, "quest_1")

        try:
            await update_balance(session, callback_query.from_user.id, profit=1200)
            await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'+1200 на балансе😉', show_alert=True)
        except Exception as e:
            logger.error(f"Ошибка: {e}. Пользователь: {callback_query.from_user.username} ({callback_query.from_user.id})")

    except Exception as e:
            logger.error(f"Ошибка: {e}. Пользователь: {callback_query.from_user.username} ({callback_query.from_user.id})")
    else:
        await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Подпишись на @TONKOFFchat_ru пробуй еще раз', show_alert=True)
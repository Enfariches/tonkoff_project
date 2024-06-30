from aiogram.types import CallbackQuery
from aiogram import F

from config import dp, bot, logger
import board as b

from database.db_bot import update_canal_en_check, update_balance, check_canal_en_status

@dp.callback_query(F.data == "Канал_en")
async def query_handler(callback_query: CallbackQuery):

    await bot.send_message(chat_id=callback_query.from_user.id, text=f"Subscribe, if you want to receive an Airdrop!💸 \n", reply_markup=b.en_channel_board)
    await callback_query.message.delete()

@dp.callback_query(F.data == "Проверка_канал_en")
async def query_handler(callback_query: CallbackQuery):

    try:
        already_checked = await check_canal_en_status(user_username=callback_query.from_user.username)
        if already_checked:
            await bot.answer_callback_query(callback_query_id=callback_query.id, text='You have already received points for subscribing to this channel', show_alert=True)
            return
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователь: {callback_query.from_user.username} ({callback_query.from_user.id})")

    try:
        user_channel_status_en = await bot.get_chat_member(chat_id='@aleg_tonkoff_en', user_id=callback_query.from_user.id)
    except Exception as e:
        logger.warning(f"Ошибка: {e}. Пользователь: {callback_query.from_user.username} ({callback_query.from_user.id})")

    if user_channel_status_en.status != "left":

        try:
            await update_canal_en_check(user_username=callback_query.from_user.username)

            try:
                await update_balance(profit=1000, user_username=callback_query.from_user.username)
                await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'+rep +vibe +1000😘', show_alert=True)
            except Exception as e:
                logger.error(f"Ошибка: {e}. Пользователь: {callback_query.from_user.username} ({callback_query.from_user.id})")
                
        except Exception as e:
            logger.error(f"Ошибка: {e}. Пользователь: {callback_query.from_user.username} ({callback_query.from_user.id})")
    else:
        await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Subscribe @aleg_tonkoff_en and try again', show_alert=True)
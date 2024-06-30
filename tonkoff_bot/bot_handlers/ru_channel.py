from aiogram.types import CallbackQuery
from aiogram import F

from config import dp, bot, logger
import board as b

from database.db_bot import update_canal_ru_check, check_canal_ru_status, update_balance

@dp.callback_query(F.data == "Канал_ru")
async def query_handler(callback_query: CallbackQuery):

    await bot.send_message(chat_id=callback_query.from_user.id, text=f"Пдпишись на канал, если хочешь получить Airdrop!💸 \n", reply_markup=b.ru_channel_board)
    await callback_query.message.delete()

@dp.callback_query(F.data == "Проверка_канал_ru")
async def query_handler(callback_query: CallbackQuery):

    try:
        already_checked = await check_canal_ru_status(user_username=callback_query.from_user.username)
        if already_checked:
            await bot.answer_callback_query(callback_query_id=callback_query.id,
                                        text='Вы уже получили очки за подписку на этот канал.', show_alert=True)
            return
    except Exception as e:
            logger.error(f"Ошибка: {e}. Пользователь: {callback_query.from_user.username} ({callback_query.from_user.id})")

    try:        
        user_channel_status_ru = await bot.get_chat_member(chat_id='@aleg_tonkoff', user_id=callback_query.from_user.id)
    except Exception as e:
        logger.warning(f"Ошибка: {e}. Пользователь: {callback_query.from_user.username} ({callback_query.from_user.id})")

    if user_channel_status_ru.status != "left":

        try:
            await update_canal_ru_check(user_username=callback_query.from_user.username)

            try:
                await update_balance(profit=1000, user_username=callback_query.from_user.username)
                await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Держи косарик, бро!😘', show_alert=True)
            except Exception as e:
                logger.error(f"Ошибка: {e}. Пользователь: {callback_query.from_user.username} ({callback_query.from_user.id})")

        except Exception as e:
            logger.error(f"Ошибка: {e}. Пользователь: {callback_query.from_user.username} ({callback_query.from_user.id})")
    else:
        await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Подпишись на @aleg_tonkoff пробуй еще раз', show_alert=True)
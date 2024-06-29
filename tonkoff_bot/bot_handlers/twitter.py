from aiogram.types import CallbackQuery
from aiogram import F

from config import dp, bot
import board as b

from database.db_bot import update_twitter_check, update_balance, check_twitter_status

@dp.callback_query(F.data == "Twitter")
async def query_handler(callback_query: CallbackQuery):
    try:
        await bot.send_message(chat_id=callback_query.from_user.id, text="Follow the news!", reply_markup=b.twitter_board)
        await callback_query.message.delete()
    except:
        await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка получения ссылки на X.com")

@dp.callback_query(F.data == "Проверка_twitter")
async def query_handler(callback_query: CallbackQuery):
    already_checked = await check_twitter_status(user_username=callback_query.from_user.username)
    if already_checked:
        await bot.answer_callback_query(callback_query_id=callback_query.id,
                                        text='You have already received points for subscribing', show_alert=True)
        return
    try:
        await update_twitter_check(user_username=callback_query.from_user.username)
        await update_balance(profit=1200, user_username=callback_query.from_user.username)
        await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'+1200 на балансе😉', show_alert=True)
    except Exception as e:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка обновления баланса")
    else:
        await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Подпишись на @TONKOFFchat_ru пробуй еще раз', show_alert=True)
from aiogram.types import CallbackQuery
from aiogram import F

from config import dp, bot
import board as b

from database.db_bot import update_chat_en_check, update_balance, check_chat_en_status

@dp.callback_query(F.data == "Чат_en")
async def query_handler(callback_query: CallbackQuery):
    try:
        await bot.send_message(chat_id=callback_query.from_user.id, text="With these people you will make money!💵", reply_markup=b.en_chat_board)
        await callback_query.message.delete()
    except:
        await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка получения ссылки на канал")

dp.callback_query(F.data == "Проверка_чат_en")
async def query_handler(callback_query: CallbackQuery):
    already_checked = await check_chat_en_status(user_username=callback_query.from_user.username)
    if already_checked:
        await bot.answer_callback_query(callback_query_id=callback_query.id,
                                        text='Вы уже получили очки за подписку на этот чат.', show_alert=True)
        return
    user_channel_status_en = await bot.get_chat_member(chat_id=417908989, user_id=callback_query.from_user.id)
    if user_channel_status_en.status != "left":
        try:
            await update_chat_en_check(user_username=callback_query.from_user.username)
            await update_balance(profit=700, user_username=callback_query.from_user.username)
            await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'+700 social credit🫂', show_alert=True)
        except Exception as e:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка обновления баланса")
    else:
        await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Subscribe @TONKOFFchat_EN and try again', show_alert=True)
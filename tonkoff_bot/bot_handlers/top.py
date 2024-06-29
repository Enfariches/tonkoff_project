from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F

from config import dp, bot
import board as b

from database.db_bot import get_top_50_users

@dp.callback_query(F.data == "Топ")
async def query_handler(callback_query: CallbackQuery, state: FSMContext):
    try:
        top_users = await get_top_50_users()
        if not top_users:
            await bot.send_message(chat_id=callback_query.from_user.id, text="Топ пользователей пока пуст.")
            return

        leaderboard = "\n".join([f"{idx + 1}. {user[0]}: {user[1]} points" for idx, user in enumerate(top_users)])
        await bot.send_message(chat_id=callback_query.from_user.id,
                                text=f"🏆 Топ 50 пользователей:\n\n{leaderboard}", reply_markup=b.back_board)
        await callback_query.message.delete()
    except Exception as e:
        await bot.send_message(chat_id=callback_query.from_user.id, text="Ошибка получения топа пользователей")
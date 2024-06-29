from aiogram.types import CallbackQuery, FSInputFile
from aiogram import F

from config import dp, bot
import board as b

from database.db_bot import update_friends_balance, update_friends_score, get_friends_balance
from database.db_bot import get_friends_score_profile, get_invited_users, get_count_profile

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

@dp.callback_query(F.data == "Мои")
async def query_handler(callback_query: CallbackQuery):
    try:
        await update_friends_score()
        friends_score = await get_friends_score_profile(callback_query.from_user.username)
        bonus_score = friends_score * 0.3

        await update_friends_balance()
        friends_balance = await get_friends_balance(callback_query.from_user.username)
        bonus_balance = friends_balance * 0.3

        total_bonus = bonus_balance + bonus_score
        total_bonus_round = toFixed(total_bonus)

        count = await get_count_profile(callback_query.from_user.username)
        invited_users = await get_invited_users(user_username = callback_query.from_user.username)
        friends_score = await get_friends_score_profile(callback_query.from_user.username)

        invited_users_str = '\n'.join([f"{idx + 1}. {user[0]}: {user[1]} points" for idx, user in enumerate(invited_users)])
        await bot.send_photo(chat_id=callback_query.from_user.id,
                                photo=FSInputFile(path="tonkoff_bot/assets/ref_link_picture.jpg"),
                                caption=f"Количество приглашенных партнеров: {count} 🤝\nОни приносят тебе: {total_bonus_round} points\n\nСмотри, сколько они набрали👇\n{invited_users_str}",
                                reply_markup=b.menu_board)
        await callback_query.message.delete()
    except Exception as e:
        await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка получения кол-во приглашенных пользователей")

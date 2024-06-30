from aiogram.types import CallbackQuery, FSInputFile
from aiogram import F

from config import dp, bot, logger
import board as b

from database.db_bot import update_friends_balance, update_friends_score, get_friends_balance
from database.db_bot import get_friends_score_profile, get_invited_users, get_count_profile

@dp.callback_query(F.data == "Мои")
async def query_handler(callback_query: CallbackQuery):

    try:
        await update_friends_score()
        bonus_score = await get_friends_score_profile(callback_query.from_user.username) * 0.3
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {callback_query.from_user.username} ({callback_query.from_user.id})")
    
    try:
        await update_friends_balance()
        bonus_balance = await get_friends_balance(callback_query.from_user.username) * 0.3
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {callback_query.from_user.username} ({callback_query.from_user.id})")

    total_bonus = round(bonus_balance + bonus_score, 1) #Отображаем

    try:
        count = await get_count_profile(callback_query.from_user.username)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {callback_query.from_user.username} ({callback_query.from_user.id})")

    try:
        invited_users = await get_invited_users(callback_query.from_user.username)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {callback_query.from_user.username} ({callback_query.from_user.id})")

    invited_users_str = '\n'.join([f"{idx + 1}. {user[0]}: {user[1]} points" for idx, user in enumerate(invited_users)]) #Отображаем
    await bot.send_photo(chat_id=callback_query.from_user.id,
                            photo=FSInputFile(path="tonkoff_bot/assets/ref_link_picture.jpg"),
                            caption=f"Количество приглашенных партнеров: {count} 🤝\nОни приносят тебе: {total_bonus} points\n\nСмотри, сколько они набрали👇\n{invited_users_str}",
                            reply_markup=b.menu_board)
    await callback_query.message.delete()

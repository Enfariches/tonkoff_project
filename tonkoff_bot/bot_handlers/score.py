from aiogram.types import CallbackQuery, FSInputFile
from aiogram import F

from config import dp, bot, logger
import board as b

from database.db_bot import get_user_score_profile, get_wallet_address, get_balance_profile, get_friends_score_profile
from database.db_bot import update_total, get_friends_balance, update_friends_score, update_friends_balance

@dp.callback_query(F.data == "Счет")
async def query_handler(callback_query: CallbackQuery):

    try:
        user_score = await get_user_score_profile(callback_query.from_user.username)
        user_balance = await get_balance_profile(callback_query.from_user.username)
        wallet = await get_wallet_address(callback_query.from_user.username)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {callback_query.from_user.username} ({callback_query.from_user.id})")
    
    try:
        await update_friends_score()
        bonus_score = await get_friends_score_profile(callback_query.from_user.username) * 0.3
        bonus_score_sum = round(bonus_score + user_score, 1)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {callback_query.from_user.username} ({callback_query.from_user.id})")
    
    try:
        await update_friends_balance()
        bonus_balance = await get_friends_balance(callback_query.from_user.username) * 0.3
        bonus_balance_sum = round(bonus_balance, 1)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {callback_query.from_user.username} ({callback_query.from_user.id})")

    total_bonus = bonus_balance_sum + bonus_balance_sum + user_balance
    try:
        await update_total(total_bonus, user_username=callback_query.from_user.username)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {callback_query.from_user.username} ({callback_query.from_user.id})")

    await bot.send_photo(chat_id=callback_query.from_user.id,
                            photo=FSInputFile(path="tonkoff_bot/assets/points_picture.jpg"),
                            caption=f"Очков в кликере: {user_score} Points\nЗа клики рефералов: {bonus_score_sum} Points\n\n"
                                    f"Очков за задания {user_balance} Points\nЗа задания рефералов: {bonus_balance_sum} Points\n\n"
                                    f"Total: {total_bonus}  Points\n\nWallet: {wallet}",
                            reply_markup=b.wallet_board)
    await callback_query.message.delete()
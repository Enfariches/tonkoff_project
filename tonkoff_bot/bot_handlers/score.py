from aiogram.types import CallbackQuery, FSInputFile
from aiogram import F

from config import dp, bot, logger
import board as b

from database.db_bot import get_field, update_total
from database.db_bot import update_friends_score, update_friends_balance

from sqlalchemy.ext.asyncio import AsyncSession

@dp.callback_query(F.data == "Счет")
async def query_handler(callback_query: CallbackQuery, session: AsyncSession):

    try:
        user_score = await get_field(session, callback_query.from_user.id, "user_score")
        user_balance = await get_field(session, callback_query.from_user.id, "balance")
        wallet = await get_field(session, callback_query.from_user.id, "wallet_address")
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {callback_query.from_user.username} ({callback_query.from_user.id})")
    
    try:
        await update_friends_score(session, callback_query.from_user.id)
        bonus_score = await get_field(session, callback_query.from_user.id, "friends_score") * 0.3
        bonus_score_sum = round(bonus_score + user_score, 1)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {callback_query.from_user.username} ({callback_query.from_user.id})")
    
    try:
        await update_friends_balance(session, callback_query.from_user.id)
        bonus_balance = await get_field(session, callback_query.from_user.id, "friends_balance") * 0.3
        bonus_balance_sum = round(bonus_balance, 1)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {callback_query.from_user.username} ({callback_query.from_user.id})")

    total_bonus = bonus_balance_sum + bonus_balance_sum + user_balance

    try:
        await update_total(session, callback_query.from_user.id, total_bonus)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {callback_query.from_user.username} ({callback_query.from_user.id})")

    await bot.send_photo(chat_id=callback_query.from_user.id,
                            photo=FSInputFile(path="tonkoff_bot/assets/points_picture.jpg"),
                            caption=f"Очков в кликере: {user_score} Points\nЗа клики рефералов: {bonus_score_sum} Points\n\n"
                                    f"Очков за задания {user_balance} Points\nЗа задания рефералов: {bonus_balance_sum} Points\n\n"
                                    f"Total: {total_bonus}  Points\n\nWallet: {wallet}",
                            reply_markup=b.wallet_board)
    await callback_query.message.delete()
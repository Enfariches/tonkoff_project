from aiogram.types import CallbackQuery, FSInputFile
from aiogram import F

from config import dp, bot
import board as b

from database.db_bot import get_user_score_profile, get_wallet_address, get_balance_profile, get_friends_score_profile
from database.db_bot import update_total, get_friends_balance, update_friends_score, update_friends_balance

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

@dp.callback_query(F.data == "Счет")
async def query_handler(callback_query: CallbackQuery):
    try:
        user_score = await get_user_score_profile(callback_query.from_user.username)
        wallet = await get_wallet_address(callback_query.from_user.username)
        balance = await get_balance_profile(callback_query.from_user.username)

        await update_friends_score()
        friends_score = await get_friends_score_profile(callback_query.from_user.username)
        bonus_score = friends_score * 0.3
        sum_score = bonus_score + user_score
        bonus_score_round = toFixed(bonus_score)
        sum_score_round = toFixed(sum_score)

        await update_friends_balance()
        friends_balance = await get_friends_balance(callback_query.from_user.username)
        bonus_balance = friends_balance * 0.3
        sum_balance = bonus_balance + balance
        bonus_balance_round = toFixed(bonus_balance)
        sum_balance_round = toFixed(sum_balance)

        total_bonus = bonus_balance + bonus_score
        total = sum_balance + sum_score
        total_bonus_round = toFixed(total_bonus)
        total_round = toFixed(total)

        await update_total(total, user_username=callback_query.from_user.username)

        await bot.send_photo(chat_id=callback_query.from_user.id,
                                photo=FSInputFile(path="tonkoff_bot/assets/points_picture.jpg"),
                                caption=f"Очков в кликере: {user_score} Points\nЗа клики рефералов: {bonus_score_round} Points\n\n"
                                        f"Очков за задания {balance} Points\nЗа задания рефералов: {bonus_balance_round} Points\n\n"
                                        f"Total: {total_round}  Points\n\nWallet: {wallet}",
                                reply_markup=b.wallet_board)
        await callback_query.message.delete()
    except Exception as e:
        await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка получения баланса")
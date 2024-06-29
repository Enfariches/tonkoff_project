from aiogram.types import CallbackQuery, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F

from config import dp, bot
import board as b

def webapp_builder(user_username: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Разомни пальцы!',
        web_app=WebAppInfo(url=f'https://354d-2a00-1fa2-4111-a3ad-2967-866a-3d54-7bd2.ngrok-free.app/?user={user_username}')
    )
    return builder.as_markup()

@dp.callback_query(F.data == "Кликер")
async def query_handler(callback_query: CallbackQuery):
    user_username = callback_query.from_user.username
    try:
        await bot.send_message(chat_id=callback_query.from_user.id,
                                text="Открыть кликер💰(beta)",
                                reply_markup=webapp_builder(user_username)
                                )
    except Exception as e:
        await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка авторизации")
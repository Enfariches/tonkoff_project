from aiogram.types import CallbackQuery
from main import bot

async def query_test(callback_query: CallbackQuery):
    if callback_query.data == "Тест":
        bot.send_message(chat_id=callback_query.from_user.id, text=f"Тест сработал")
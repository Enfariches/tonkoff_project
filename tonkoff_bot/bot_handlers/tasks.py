from aiogram.types import CallbackQuery, FSInputFile
from aiogram import F

from config import dp, bot
import board as b

@dp.callback_query(F.data == "Задания")
async def query_handler(callback_query: CallbackQuery):

    await bot.send_photo(chat_id=callback_query.from_user.id, photo=FSInputFile(path="tonkoff_bot/assets/tasks_picture.jpg"), reply_markup=b.tasks_board)
    await callback_query.message.delete()
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F

from config import dp, bot

from wallet_handlers.wallet_state import *

@dp.callback_query(F.data == "Wallet")
async def query_handler(callback_query: CallbackQuery, state: FSMContext):
    try:
        await bot.send_message(chat_id=callback_query.from_user.id, text="Введите адрес вашего TON-кошелька:")
        await state.set_state(WalletState.waiting_for_wallet_address)
        await callback_query.message.delete()
    except:
        await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка добавления адреса")
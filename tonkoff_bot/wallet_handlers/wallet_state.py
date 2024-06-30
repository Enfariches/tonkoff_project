from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext

from config import dp, bot, logger
import board as b

from database.db_bot import update_wallet_address, update_message, get_message, get_all_user_ids

class WalletState(StatesGroup):
    waiting_for_wallet_address = State()
    waiting_for_text = State()
    waiting_for_photo = State()

@dp.message(WalletState.waiting_for_wallet_address)
async def wallet_address_received(message: Message, state: FSMContext):

    wallet_address = message.text

    try:
        await update_wallet_address(wallet_address, message.from_user.username)
        await message.answer("Ваш адрес успешно сохранен!")
        await bot.send_photo(chat_id=message.from_user.id,
                            photo=FSInputFile(path="tonkoff_bot/assets/status_picture.jpg"), reply_markup=b.menu_board)
        await state.clear()
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {message.from_user.username} ({message.from_user.id})")

@dp.message(WalletState.waiting_for_text)
async def handle_broadcast_message(message: Message, state: FSMContext):
    
    text = message.text

    try:
        await update_message(user_username=message.from_user.username, admin_message = text)
        await message.reply("Пришлите фото для рассылки")
        await state.set_state(WalletState.waiting_for_photo)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {message.from_user.username} ({message.from_user.id})")

@dp.message(WalletState.waiting_for_photo)
async def handle_broadcast_photo(message: Message, state: FSMContext):

    photo = message.photo[-1]
    photo_id = photo.file_id
    
    try:
        text = await get_message(user_username=message.from_user.username)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {message.from_user.username} ({message.from_user.id})")

    try:
        all_users = await get_all_user_ids()
        for user_id in all_users:
            try:
                await bot.send_photo(chat_id=user_id, photo=photo_id, caption=text)
            except Exception as e:
                print(f"Failed to send message to {user_id}: {e}")
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {message.from_user.username} ({message.from_user.id})")

    await message.reply("Рассылка отправлена")
    await state.clear()
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup

from config import bot, dp, logger, ADMIN_USER_ID
import board as b

from database.db_bot import create_message, update_message, update_wallet_address, get_message, get_all_user_ids
from sqlalchemy.ext.asyncio import AsyncSession

class WalletState(StatesGroup):
    waiting_for_wallet_address = State()
    waiting_for_text = State()
    waiting_for_photo = State()

@dp.message(Command("send"))
async def broadcast_message(message: Message, state: FSMContext, session: AsyncSession):
    
    try:
        if message.from_user.id in ADMIN_USER_ID:
            await message.reply("Пришлите текст для рассылки")
            await create_message(session, message.from_user.id)
            await state.set_state(WalletState.waiting_for_text)
        else:
            await message.reply("Вы не админ")
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователь: {message.from_user.username} ({message.from_user.id})")

@dp.message(WalletState.waiting_for_wallet_address)
async def wallet_address_received(message: Message, state: FSMContext, session: AsyncSession):

    wallet_address = message.text

    try:
        await update_wallet_address(session, message.from_user.id, wallet_address)
        await message.answer("Ваш адрес успешно сохранен!")
        await bot.send_photo(chat_id=message.from_user.id,
                            photo=FSInputFile(path="tonkoff_bot/assets/status_picture.jpg"), reply_markup=b.menu_board)
        await state.clear()
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {message.from_user.username} ({message.from_user.id})")

@dp.message(WalletState.waiting_for_text)
async def handle_broadcast_message(message: Message, state: FSMContext, session: AsyncSession):

    try:
        await update_message(session, message.from_user.id, message.text)
        await message.reply("Пришлите фото для рассылки")
        await state.set_state(WalletState.waiting_for_photo)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {message.from_user.username} ({message.from_user.id})")

@dp.message(WalletState.waiting_for_photo)
async def handle_broadcast_photo(message: Message, state: FSMContext, session: AsyncSession):

    photo = message.photo[-1]
    photo_id = photo.file_id
    
    try:
        text = await get_message(session, message.from_user.id)
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {message.from_user.username} ({message.from_user.id})")

    try:
        all_users = await get_all_user_ids(session)
        for user_id in all_users:
            try:
                await bot.send_photo(chat_id=user_id, photo=photo_id, caption=text)
            except Exception as e:
                logger.error(f"Ошибка: {e}. Не удалось отправить сообщения {user_id})")
                print(f"Failed to send message to {user_id}: {e}")
    except Exception as e:
        logger.error(f"Ошибка: {e}. Пользователя: {message.from_user.username} ({message.from_user.id})")

    await message.reply("Рассылка отправлена")
    await state.clear()
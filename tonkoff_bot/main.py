import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, WebAppInfo, InlineKeyboardMarkup, FSInputFile
from aiogram.filters import CommandStart
from aiogram.utils.deep_linking import create_start_link, decode_payload
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from commands.handler_test import query_test

import board as b
from database.db_bot import *

ADMIN_USER_ID = (1311520715, 7017020568, 6109091581)
bot = Bot(token="7016938804:AAGD63uy5q-2fkwv8UrCy5V656nJqC7rEBM")
dp = Dispatcher()

class WalletState(StatesGroup):
    waiting_for_wallet_address = State()
    waiting_for_text = State()
    waiting_for_photo = State()

@dp.message(WalletState.waiting_for_wallet_address)
async def wallet_address_received(message: Message, state: FSMContext):
    wallet_address = message.text
    await update_wallet_address(wallet_address, message.from_user.username)
    await message.answer("Ваш адрес успешно сохранен!")
    await bot.send_photo(chat_id=message.from_user.id,
                         photo=FSInputFile(path="status_picture.jpg"), reply_markup=b.board1)
    await state.clear()

def webapp_builder(user_username: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text='Разомни пальцы!',
        web_app=WebAppInfo(url=f'https://grubworm-ultimate-griffon.ngrok-free.app/?user={user_username}')
    )
    return builder.as_markup()

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"

@dp.message(Command("send"))
async def broadcast_message(message: Message, state: FSMContext):
    if message.from_user.id in ADMIN_USER_ID:
        await message.reply("Пришлите текст для рассылки")
        await create_message(user_username=message.from_user.username)
        await state.set_state(WalletState.waiting_for_text)
    else:
        await message.reply("Вы не админ")

@dp.message(WalletState.waiting_for_text)
async def handle_broadcast_message(message: Message, state: FSMContext):
    text = message.text
    await update_message(user_username=message.from_user.username, admin_message = text)
    await message.reply("Пришлите фото для рассылки")
    await state.set_state(WalletState.waiting_for_photo)

@dp.message(WalletState.waiting_for_photo)
async def handle_broadcast_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]
    photo_id = photo.file_id

    text = await get_message(user_username=message.from_user.username)

    all_users = await get_all_user_ids()
    for user_id in all_users:
        try:
            await bot.send_photo(chat_id=user_id, photo=photo_id, caption=text)
        except Exception as e:
            print(f"Failed to send message to {user_id}: {e}")

    await message.reply("Рассылка отправлена")
    await state.clear()

@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    try:
        args = message.text.split(' ')[1]
        payload = decode_payload(args)
    except Exception as e:
        payload = ""
    try:
        await create_profile(user_username=message.from_user.username, user_id=message.from_user.id, payload=payload)
        await create_check_user(user_username=message.from_user.username, user_id=message.from_user.id)
    except Exception as e:
        await message.answer(f"Ошибка добавления профиля")

    user_username = message.from_user.username
    greeting_message = (f"Салют, {user_username}, вот и настало твое время становиться миллионером!✈️ \n"
                        f"Начни свой путь правильно:\n"
                        f"· Присоединяйся к нашему каналу @aleg_tonkoff\n"
                        f"· Разомни свои пальчики в кликере и заработай немного деньжат\n"
                        f"· Приглашай бизнес-партнеров \n"
                        f"Осмотрись тут, потягивая джин-тоник")
    await bot.send_photo(chat_id=message.from_user.id, photo=FSInputFile(path="tonkoff_bot/assets/start_picture.jpg"), caption=greeting_message, reply_markup=b.start_board)

@dp.callback_query()
async def query_keyboard(callback_query: CallbackQuery, state: FSMContext):
    
    query_test(callback_query=callback_query)

    if callback_query.data == "Рефка":
        link = await create_start_link(bot=bot, payload=str(callback_query.from_user.username), encode=True)
        try:
            await update_link_profile(user_username=callback_query.from_user.username, ref_link=link)
            await bot.send_photo(chat_id=callback_query.from_user.id, photo=FSInputFile(path="tonkoff_bot/assets/ref_picture.jpg"), caption=f"Твоя ссылка для приглашения партнеров: {link}\n\nТы будешь получать 30% от всех их $Tonkoff points!📈",
                                                                                        reply_markup=b.board1)
            await callback_query.message.delete()
        except Exception as e:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка добавления рефки")

    elif callback_query.data == "Счет":
        try:
            user_score = await get_user_score_profile(callback_query.from_user.username)
            wallet = await get_wallet_address(callback_query.from_user.username)
            balance = await get_balance_profile(callback_query.from_user.username)

            await update_friends_score()
            friends_score = await get_friends_score_profile(callback_query.from_user.username)
            bonus_score = friends_score*0.3
            sum_score = bonus_score + user_score
            bonus_score_round = toFixed(bonus_score)
            sum_score_round = toFixed(sum_score)

            await update_friends_balance()
            friends_balance = await get_friends_balance(callback_query.from_user.username)
            bonus_balance = friends_balance*0.3
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
                                 reply_markup=b.board4)
            await callback_query.message.delete()
        except Exception as e:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка получения баланса")

    elif callback_query.data == "Мои":
        try:
            await update_friends_score()
            friends_score = await get_friends_score_profile(callback_query.from_user.username)
            bonus_score = friends_score * 0.3

            await update_friends_balance()
            friends_balance = await get_friends_balance(callback_query.from_user.username)
            bonus_balance = friends_balance * 0.3

            total_bonus = bonus_balance + bonus_score
            total_bonus_round = toFixed(total_bonus)

            count = await get_count_profile(callback_query.from_user.username)
            invited_users = await get_invited_users(user_username = callback_query.from_user.username)
            friends_score = await get_friends_score_profile(callback_query.from_user.username)

            invited_users_str = '\n'.join([f"{idx + 1}. {user[0]}: {user[1]} points" for idx, user in enumerate(invited_users)])
            await bot.send_photo(chat_id=callback_query.from_user.id,
                                 photo=FSInputFile(path="tonkoff_bot/assets/ref_link_picture.jpg"),
                                 caption=f"Количество приглашенных партнеров: {count} 🤝\nОни приносят тебе: {total_bonus_round} points\n\nСмотри, сколько они набрали👇\n{invited_users_str}",
                                 reply_markup=b.board1)
            await callback_query.message.delete()
        except Exception as e:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка получения кол-во приглашенных пользователей")

    elif callback_query.data == "Задания":
        try:
            await bot.send_photo(chat_id=callback_query.from_user.id, photo=FSInputFile(path="tonkoff_bot/assets/tasks_picture.jpg"), reply_markup=b.board2)
            await callback_query.message.delete()
        except Exception as e:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка получения заданий")

    elif callback_query.data == "Канал_ru":
        try:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Подпишись на канал, если хочешь получить Airdrop!💸 \n", reply_markup=b.board31)
            await callback_query.message.delete()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка получения ссылки на канал")

    elif callback_query.data == "Канал_en":
        try:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Subscribe, if you want to receive an Airdrop!💸 \n", reply_markup=b.board32)
            await callback_query.message.delete()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка получения ссылки на канал")

    elif callback_query.data == "Проверка_канал_ru":
        already_checked = await check_canal_ru_status(user_username=callback_query.from_user.username)
        if already_checked:
            await bot.answer_callback_query(callback_query_id=callback_query.id,
                                            text='Вы уже получили очки за подписку на этот канал.', show_alert=True)
            return
        user_channel_status_ru = await bot.get_chat_member(chat_id='@aleg_tonkoff', user_id=callback_query.from_user.id)
        if user_channel_status_ru.status != "left":
            try:
                await update_canal_ru_check(user_username=callback_query.from_user.username)
                await update_balance(profit=1000, user_username=callback_query.from_user.username)
                await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Держи косарик, бро!😘', show_alert=True)
            except Exception as e:
                await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка обновления баланса")
        else:
            await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Подпишись на @aleg_tonkoff пробуй еще раз', show_alert=True)

    elif callback_query.data == "Проверка_канал_en":
        already_checked = await check_canal_en_status(user_username=callback_query.from_user.username)
        if already_checked:
            await bot.answer_callback_query(callback_query_id=callback_query.id, text='You have already received points for subscribing to this channel', show_alert=True)
            return
        user_channel_status_en = await bot.get_chat_member(chat_id='@aleg_tonkoff_en', user_id=callback_query.from_user.id)
        if user_channel_status_en.status != "left":
            try:
                await update_canal_en_check(user_username=callback_query.from_user.username)
                await update_balance(profit=1000, user_username=callback_query.from_user.username)
                await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'+rep +vibe +1000😘', show_alert=True)
            except Exception as e:
                await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка обновления баланса")
        else:
            await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Subscribe @aleg_tonkoff_en and try again', show_alert=True)

    elif callback_query.data == "Чат_ru":
        try:
            await bot.send_message(chat_id=callback_query.from_user.id, text="С этими людьми ты заработаешь!💵", reply_markup=b.board_chat_ru)
            await callback_query.message.delete()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка получения ссылки на канал")

    elif callback_query.data == "Чат_en":
        try:
            await bot.send_message(chat_id=callback_query.from_user.id, text="With these people you will make money!💵", reply_markup=b.board_chat_en)
            await callback_query.message.delete()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка получения ссылки на канал")

    elif callback_query.data == "Проверка_чат_ru":
        already_checked = await check_chat_ru_status(user_username=callback_query.from_user.username)
        if already_checked:
            await bot.answer_callback_query(callback_query_id=callback_query.id,
                                            text='You have already received points for subscribing to this chat', show_alert=True)
            return
        user_channel_status_ru = await bot.get_chat_member(chat_id=-1002152050429, user_id=callback_query.from_user.id)
        if user_channel_status_ru.status != "left":
            try:
                await update_chat_ru_check(user_username=callback_query.from_user.username)
                await update_balance(profit=700, user_username=callback_query.from_user.username)
                await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'+700 на балансе😉', show_alert=True)
            except Exception as e:
                await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка обновления баланса")
        else:
            await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Подпишись на @TONKOFFchat_ru пробуй еще раз', show_alert=True)

    elif callback_query.data == "Проверка_чат_en":
        already_checked = await check_chat_en_status(user_username=callback_query.from_user.username)
        if already_checked:
            await bot.answer_callback_query(callback_query_id=callback_query.id,
                                            text='Вы уже получили очки за подписку на этот чат.', show_alert=True)
            return
        user_channel_status_en = await bot.get_chat_member(chat_id=-1002189061544, user_id=callback_query.from_user.id)
        if user_channel_status_en.status != "left":
            try:
                await update_chat_en_check(user_username=callback_query.from_user.username)
                await update_balance(profit=700, user_username=callback_query.from_user.username)
                await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'+700 social credit🫂', show_alert=True)
            except Exception as e:
                await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка обновления баланса")
        else:
            await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Subscribe @TONKOFFchat_EN and try again', show_alert=True)

    elif callback_query.data == "Twitter":
        try:
            await bot.send_message(chat_id=callback_query.from_user.id, text="Follow the news!", reply_markup=b.board_twitter)
            await callback_query.message.delete()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка получения ссылки на X.com")

    elif callback_query.data == "Проверка_twitter":
        already_checked = await check_twitter_status(user_username=callback_query.from_user.username)
        if already_checked:
            await bot.answer_callback_query(callback_query_id=callback_query.id,
                                            text='You have already received points for subscribing', show_alert=True)
            return
        try:
            await update_twitter_check(user_username=callback_query.from_user.username)
            await update_balance(profit=1200, user_username=callback_query.from_user.username)
            await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'+1200 на балансе😉', show_alert=True)
        except Exception as e:
                await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка обновления баланса")
        else:
            await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Подпишись на @TONKOFFchat_ru пробуй еще раз', show_alert=True)

    elif callback_query.data == "Назад":
        await bot.send_photo(chat_id=callback_query.from_user.id,
                             photo=FSInputFile(path="tonkoff_bot/assets/status_picture.jpg"),
                             reply_markup=b.board1)
        await callback_query.message.delete()

    elif callback_query.data == "Кликер":
        user_username = callback_query.from_user.username
        try:
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text="Открыть кликер💰(beta)",
                                   reply_markup=webapp_builder(user_username)
                                   )

        except Exception as e:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка авторизации")

    elif callback_query.data == "Начать":
        user_channel_status_ru = await bot.get_chat_member(chat_id='@myfavhero', user_id=callback_query.from_user.id) #Изменить в конце на TONKOFF
        if user_channel_status_ru.status != "left":
            try:
                await update_canal_ru_check(user_username=callback_query.from_user.username)
                await bot.send_photo(chat_id=callback_query.from_user.id,
                                     photo=FSInputFile(path="tonkoff_bot/assets/status_picture.jpg"),
                                     reply_markup=b.board1)
                await callback_query.message.delete()
            except Exception as e:
                await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка получения статуса {e}")

        elif user_channel_status_en.status != "left":
            try:
                await update_canal_en_check(user_username=callback_query.from_user.username)
                await update_balance(profit=1000, user_username=callback_query.from_user.username)
                await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'sUp, br0!🐤', show_alert=True)
                await bot.send_photo(chat_id=callback_query.from_user.id,
                                     photo=FSInputFile(path="tonkoff_bot/assets/status_picture.jpg"),
                                     reply_markup=b.board1)
            except Exception as e:
                await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка получения статуса {e}")
        else:
            await bot.answer_callback_query(callback_query_id=callback_query.id, text=f'Вы не подписались на канал https://t.me/aleg_tonkoff', show_alert=True)

    elif callback_query.data == "Wallet":
        try:
            await bot.send_message(chat_id=callback_query.from_user.id, text="Введите адрес вашего TON-кошелька:")
            await state.set_state(WalletState.waiting_for_wallet_address)
            await callback_query.message.delete()
        except:
            await bot.send_message(chat_id=callback_query.from_user.id, text=f"Ошибка добавления адреса")

    elif callback_query.data == 'Топ':
        try:
            top_users = await get_top_50_users()
            if not top_users:
                await bot.send_message(chat_id=callback_query.from_user.id, text="Топ пользователей пока пуст.")
                return

            leaderboard = "\n".join([f"{idx + 1}. {user[0]}: {user[1]} points" for idx, user in enumerate(top_users)])
            await bot.send_message(chat_id=callback_query.from_user.id,
                                   text=f"🏆 Топ 50 пользователей:\n\n{leaderboard}", reply_markup=b.board5)
            await callback_query.message.delete()
        except Exception as e:
            await bot.send_message(chat_id=callback_query.from_user.id, text="Ошибка получения топа пользователей")

async def main():
    await db_start()
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())

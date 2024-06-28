from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_button = [[InlineKeyboardButton(text="Начать", callback_data="Начать")]]
start_board = InlineKeyboardMarkup(inline_keyboard=start_button)

buttons1 = [[InlineKeyboardButton(text="Рефка", callback_data="Рефка"), InlineKeyboardButton(text="Мой счет", callback_data="Счет")],
            [InlineKeyboardButton(text="Задания", callback_data="Задания"), InlineKeyboardButton(text="Мои партнеры", callback_data="Мои")],
            [InlineKeyboardButton(text="Кликер", callback_data="Кликер"), InlineKeyboardButton(text="Тест", callback_data="Тест")]]

board1 = InlineKeyboardMarkup(inline_keyboard=buttons1)

buttons2 = [[InlineKeyboardButton(text="Подписка на канал RU (+1000 Points)", callback_data="Канал_ru")],
            [InlineKeyboardButton(text="Подписка на чат RU (+700 Points)", callback_data="Чат_ru")],
            [InlineKeyboardButton(text="Подписка на канал EN (+1000 Points)", callback_data="Канал_en")],
            [InlineKeyboardButton(text="Подписка на чат EN (+700 Points)", callback_data="Чат_en")],
            [InlineKeyboardButton(text="Подписка на Twitter (+1200 Points)", callback_data="Twitter")],
            [InlineKeyboardButton(text="Вернуться назад", callback_data="Назад")]]

board2 = InlineKeyboardMarkup(inline_keyboard=buttons2)

buttons31 = [[InlineKeyboardButton(text="Канал RU", url="https://t.me/aleg_tonkoff")],[InlineKeyboardButton(text="Проверить", callback_data="Проверка_канал_ru"), InlineKeyboardButton(text="Вернуться назад", callback_data="Задания")]]
board31 = InlineKeyboardMarkup(inline_keyboard=buttons31)

buttons32 = [[InlineKeyboardButton(text="Канал EN", url="https://t.me/aleg_tonkoff_en")],[InlineKeyboardButton(text="Проверить", callback_data="Проверка_канал_en"), InlineKeyboardButton(text="Вернуться назад", callback_data="Задания")]]
board32 = InlineKeyboardMarkup(inline_keyboard=buttons32)

buttons_chat_ru = [[InlineKeyboardButton(text="Чат RU", url="https://t.me/TONKOFF_chat_ru")],
                [InlineKeyboardButton(text="Проверить", callback_data="Проверка_чат_ru"),
                 InlineKeyboardButton(text="Вернуться назад", callback_data="Задания")]]
board_chat_ru = InlineKeyboardMarkup(inline_keyboard=buttons_chat_ru)

buttons_chat_en = [[InlineKeyboardButton(text="Чат EN", url="https://t.me/TONKOFF_chat_en")],
                [InlineKeyboardButton(text="Проверить", callback_data="Проверка_чат_en"),
                 InlineKeyboardButton(text="Вернуться назад", callback_data="Задания")]]
board_chat_en = InlineKeyboardMarkup(inline_keyboard=buttons_chat_en)

buttons_twitter = [[InlineKeyboardButton(text="X.com", url="https://x.com/AlegTonkoff")],
                [InlineKeyboardButton(text="Проверить", callback_data="Проверка_twitter"),
                 InlineKeyboardButton(text="Вернуться назад", callback_data="Задания")]]
board_twitter = InlineKeyboardMarkup(inline_keyboard=buttons_twitter)

buttons4 = [[InlineKeyboardButton(text="Wallet", callback_data="Wallet")],
            [InlineKeyboardButton(text="ТОП-50", callback_data="Топ")],
            [InlineKeyboardButton(text="Вернуться назад", callback_data="Назад")]]
board4 = InlineKeyboardMarkup(inline_keyboard=buttons4)

buttons5 = [[InlineKeyboardButton(text="Вернуться назад", callback_data="Назад")]]
board5 = InlineKeyboardMarkup(inline_keyboard=buttons5)



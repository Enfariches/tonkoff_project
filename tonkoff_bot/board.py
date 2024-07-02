from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_button = [[InlineKeyboardButton(text="Начать", callback_data="Начать")]]
start_board = InlineKeyboardMarkup(inline_keyboard=start_button)

menu_buttons = [[InlineKeyboardButton(text="Рефка", callback_data="Рефка"), InlineKeyboardButton(text="Мой счет", callback_data="Счет")],
            [InlineKeyboardButton(text="Задания", callback_data="Задания"), InlineKeyboardButton(text="Мои партнеры", callback_data="Мои")],
            [InlineKeyboardButton(text="Кликер", callback_data="Кликер")]]

menu_board = InlineKeyboardMarkup(inline_keyboard=menu_buttons)

tasks_buttons = [[InlineKeyboardButton(text="Подписка на канал RU (+1000 Points)", callback_data="Канал_ru")],
            [InlineKeyboardButton(text="Подписка на чат RU (+700 Points)", callback_data="Чат_ru")],
            [InlineKeyboardButton(text="Подписка на канал EN (+1000 Points)", callback_data="Канал_en")],
            [InlineKeyboardButton(text="Подписка на чат EN (+700 Points)", callback_data="Чат_en")],
            [InlineKeyboardButton(text="Подписка на Twitter (+1200 Points)", callback_data="Twitter")],
            [InlineKeyboardButton(text="Вернуться назад", callback_data="Назад")]]

tasks_board = InlineKeyboardMarkup(inline_keyboard=tasks_buttons)

ru_channel_buttons = [[InlineKeyboardButton(text="Канал RU", url="https://t.me/aleg_tonkoff")],[InlineKeyboardButton(text="Проверить", callback_data="Проверка_канал_ru"), InlineKeyboardButton(text="Вернуться назад", callback_data="Задания")]]
ru_channel_board = InlineKeyboardMarkup(inline_keyboard=ru_channel_buttons)

en_channel_buttons = [[InlineKeyboardButton(text="Канал EN", url="https://t.me/myfavh_ch")],[InlineKeyboardButton(text="Проверить", callback_data="Проверка_канал_en"), InlineKeyboardButton(text="Вернуться назад", callback_data="Задания")]]
en_channel_board = InlineKeyboardMarkup(inline_keyboard=en_channel_buttons)

ru_chat_buttons = [[InlineKeyboardButton(text="Чат RU", url="https://t.me/TONKOFF_chat_ru")],
                [InlineKeyboardButton(text="Проверить", callback_data="Проверка_чат_ru"),
                 InlineKeyboardButton(text="Вернуться назад", callback_data="Задания")]]
ru_chat_board = InlineKeyboardMarkup(inline_keyboard=ru_chat_buttons)

en_chat_buttons = [[InlineKeyboardButton(text="Чат EN", url="https://t.me/TONKOFF_chat_en")],
                [InlineKeyboardButton(text="Проверить", callback_data="Проверка_чат_en"),
                 InlineKeyboardButton(text="Вернуться назад", callback_data="Задания")]]
en_chat_board = InlineKeyboardMarkup(inline_keyboard=en_chat_buttons)

twitter_buttons = [[InlineKeyboardButton(text="X.com", url="https://x.com/AlegTonkoff")],
                [InlineKeyboardButton(text="Проверить", callback_data="Проверка_twitter"),
                 InlineKeyboardButton(text="Вернуться назад", callback_data="Задания")]]
twitter_board = InlineKeyboardMarkup(inline_keyboard=twitter_buttons)

wallet_buttons = [[InlineKeyboardButton(text="Wallet", callback_data="Wallet")],
            [InlineKeyboardButton(text="ТОП-50", callback_data="Топ")],
            [InlineKeyboardButton(text="Вернуться назад", callback_data="Назад")]]
wallet_board = InlineKeyboardMarkup(inline_keyboard=wallet_buttons)

back_buttons = [[InlineKeyboardButton(text="Вернуться назад", callback_data="Назад")]]
back_board = InlineKeyboardMarkup(inline_keyboard=back_buttons)



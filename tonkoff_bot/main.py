from config import dp, bot
from admin_handlers.admin import *
from database.db_bot import db_start

import asyncio
import bot_handlers

async def main():
    await db_start()
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())

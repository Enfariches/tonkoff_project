from config import dp, bot
from admin_handlers.admin import *
from middlewares.db import DataBaseSession
from database.engine import create_db, session_maker

import asyncio
import bot_handlers

async def main():
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await create_db()
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())

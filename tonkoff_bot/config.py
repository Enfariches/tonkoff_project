from aiogram import Bot, Dispatcher
import logging
from logging.handlers import RotatingFileHandler

ADMIN_USER_ID = (1311520715, 7017020568, 6109091581, 417908989)
DB_CONFIG = "postgresql+asyncpg://postgres:root@localhost:5432/bot"

bot = Bot(token="7016938804:AAGD63uy5q-2fkwv8UrCy5V656nJqC7rEBM")
dp = Dispatcher()

logger = logging.getLogger(__name__)
handler = RotatingFileHandler("bot_logs.log", maxBytes=300000000, backupCount=5, encoding="utf-8")
formatter = logging.Formatter("%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) (Func: %(funcName)s) [%(filename)s]")

handler.setFormatter(formatter)
logger.addHandler(handler)
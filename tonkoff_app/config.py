import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
handler = RotatingFileHandler("app_logs.log", maxBytes=300000000, backupCount=5, encoding="utf-8")
formatter = logging.Formatter("%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) (Func: %(funcName)s) [%(filename)s]")

handler.setFormatter(formatter)
logger.addHandler(handler)
import os 
from sqlalchemy import URL
from aiogram import Bot, Dispatcher
# from aiogram.fsm.storage.redis import RedisStorage, Redis
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from config.settings import AppConfig, RedisConfig, DATABASES, TIMEZONE
from g4f.cookies import set_cookies_dir, read_cookie_files

cookies_dir = os.path.join(os.path.dirname(__file__), "har_and_cookies")
set_cookies_dir(cookies_dir)
read_cookie_files(cookies_dir)

cfg = AppConfig().get_config()
redis_cfg = RedisConfig().get_config()
db_config = DATABASES.copy()

jobstores = {"default": SQLAlchemyJobStore(url=URL.create(**db_config))}
scheduler = AsyncIOScheduler(jobstores=jobstores, timezone=TIMEZONE)
bot = Bot(token=cfg.bot_token, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
# storage = RedisStorage(
#     redis=Redis(host=redis_cfg.host, port=redis_cfg.port, db=redis_cfg.db)
# )
dp = Dispatcher(storage=storage)

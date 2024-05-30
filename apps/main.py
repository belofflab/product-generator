from typing import Annotated
from fastapi import FastAPI, Header
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from aiogram.types import Update
from loguru import logger
from loader import dp, bot, cfg, scheduler
from config.database import DatabaseManager
from config.handlers import HandlerManager
from config.routers import RouterManager
from apps.core.utils.misc.bot_commands import set_commands
from config.settings import MEDIA_DIR, ALLOWED_HOSTS

DatabaseManager().load()


WEBHOOK_URL = cfg.web_app_domain + cfg.web_app_hook

# ----------------------------
# --- Init FastAPI Events ----
# ----------------------------

@asynccontextmanager
async def lifespan(application: FastAPI):
    scheduler.start()
    webhook = await bot.get_webhook_info()
    if webhook.url != WEBHOOK_URL:
        if not webhook.url:
            await bot.delete_webhook()
        await bot.set_webhook(WEBHOOK_URL, max_connections=40 if cfg.debug else 100, secret_token=cfg.web_app_tg_secret)
    await set_commands(bot)
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)


# ----------------------------
# --- Base Bot TG Webhook ----
# ----------------------------


@app.post(cfg.web_app_hook, include_in_schema=False)
async def bot_webhook(
    update: dict,
    x_telegram_bot_api_secret_token: Annotated[str | None, Header()] = None,
) -> None | dict:
    """Register webhook endpoint for telegram bot"""
    # if x_telegram_bot_api_secret_token != cfg.web_app_tg_secret:
    #     logger.error("Wrong secret token !")
    #     return {"status": "error", "message": "Wrong secret token !"}
    telegram_update = Update(**update)
    await dp.feed_webhook_update(bot=bot, update=telegram_update)


# ------------------
# --- Middleware ---
# ------------------


app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------
# --- Static File ---
# -------------------

# add static-file support, for see images by URL
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")


# ----------------------------
# --- Init Aiogram Routers ---
# ----------------------------

HandlerManager(dp).import_routers()


# ----------------------------
# --- Init Aiogram Tasks ----
# ----------------------------

# TaskManager().import_tasks()


# ----------------------------
# --- Init FastAPI Routers ---
# ----------------------------

RouterManager(app).import_routers()

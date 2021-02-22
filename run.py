# -*- coding: utf-8 -*-
from my_bot.bot import dp, WEBAPP_PORT, on_startup, on_shutdown, WEBAPP_HOST, WEBHOOK_PATH
from aiogram.utils.executor import start_webhook

if __name__ == "__main__":
    start_webhook(dp, WEBHOOK_PATH, on_startup, on_shutdown, True, WEBAPP_HOST, WEBAPP_PORT)
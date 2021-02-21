# -*- coding: utf-8 -*-
from bot import bot, dp
from aiogram import executor

if __name__ == "__main__":
    executor.start_polling(dp)
import time
time.sleep(7)
import asyncio
import os
import logging

from aiogram import Bot, types, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv

from middlewares.db import DataBaseSession

load_dotenv(find_dotenv())
from database.engine import create_db, drop_db, session_maker
from handlers.user_private import user_private_router
from common.bot_cmds_list import private

logging.basicConfig(level=logging.INFO)

# ALLOWED_UPDATES = ['message', 'edited_message']
# ограничиваем типы апдейтов, которые приходят к нашему боту

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
# инициализируем класс самого бота


dp = Dispatcher()
# класс, который отвечает за фильтрацию сообщений и получает
# бот от сервера телеграмм

dp.include_router(user_private_router)


async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print("бот лёг")


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)  # все, что было написано в чате до запуска бота
    # будет проигнорировано
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    # устанавливаем меню в чате
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    # метод, с помощью которого бот начнет слушать сервер телеграмм и
    # спрашивать его о наличии обновлений для него


if __name__ == '__main__':
    asyncio.run(main())

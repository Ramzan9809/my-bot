import asyncio
import os

from aiogram import Bot, Dispatcher, types

from config import TOKEN

from middlewares.db import DataBaseSession

from database.engine import create_db, drop_db, session_maker

from handlers.command import router
from handlers.admin import admin_router

# from common.bot_cmds_list import Cmds



bot = Bot(token=TOKEN)

dp = Dispatcher()



async def on_startup(bot):

    await drop_db()

    await create_db()


async def main():
    dp.include_router(router)
    dp.include_router(admin_router)
    dp.startup.register(on_startup)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    # await bot.set_my_commands(commands=Cmds, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

asyncio.run(main())
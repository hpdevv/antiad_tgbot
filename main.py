from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import middlewares
from middlewares.throttling import *
from vars import *
from database import *
import inline
from cache_deleter import delete_cache
from handlers.commands import *
from handlers.anti_osk import *

async def commands_list_menu(dp):
        await dp.bot.set_my_commands([
            types.BotCommand("start", "information"),
            types.BotCommand("report", "report"),
    ])

def register_commands():
	dp.register_message_handler(start_command, commands=['start'])
	dp.register_message_handler(report_command, commands=['report'])
	dp.register_message_handler(check_na_osk)
    
async def on_startup(dp):
	await commands_list_menu(dp)
	middlewares.setup(dp)
	delete_cache()
	register_commands()

if __name__ == '__main__':
    print("Started!")
    from aiogram import executor
    executor.start_polling(dp, on_startup=on_startup)
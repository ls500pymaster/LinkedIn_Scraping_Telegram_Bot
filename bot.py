from aiogram.utils import executor
from import_bot import dp
from handlers import client, admin, other
from database import sqlite


async def start_bot(_):
	print("Bot is online!")
	sqlite.sql_start()
	print("Database connected!")


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)
executor.start_polling(dp, skip_updates=True)

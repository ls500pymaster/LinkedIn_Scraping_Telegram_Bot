from aiogram import Bot, types, Dispatcher
from import_bot import dp, bot
from keyboards import keyboard_client
import sqlite3 as sq


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
	try:
		await bot.send_message(message.from_user.id, 'Hello. This is your answer.', reply_markup=keyboard_client)
		await message.delete()
	except:
		await message.reply('Chatting only private messages: "https://t.me/linked_offer_bot"')


# @dp.message_handler(commands=['result'])
async def command_result(message: types.Message):
	conn = sq.connect('parserdb.db')
	cursor = conn.cursor()
	result = cursor.execute('SELECT DISTINCT(name) FROM parsing ORDER BY id DESC LIMIT 10').fetchall()
	# New list
	res = [list(ele) for ele in result]
	final_res = "\n".join(str(elem) for elem in res)
	await bot.send_message(message.from_user.id, f'Last 10 contacts:\n {final_res}')


async def command_total(message: types.Message):
	conn = sq.connect('parserdb.db')
	cursor = conn.cursor()
	total = cursor.execute('SELECT name FROM parsing').fetchall()
	total_result = len(total)
	await bot.send_message(message.from_user.id, f'Total contacts added: {total_result}')


def register_handlers_client(dp: Dispatcher):
	dp.register_message_handler(command_start, commands=['start', 'help '])
	dp.register_message_handler(command_result, commands=['result'])
	dp.register_message_handler(command_total, commands=['total'])

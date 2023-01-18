from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from database import sqlite


class FSMadmin(StatesGroup):
	start_page = State()
	stop_page = State()


#  Start dialog
async def cm_start(message: types.Message):
	await FSMadmin.start_page.set()
	await message.reply('Start page')


# Exit from task
async def cancel_handler(message: types.Message, state: FSMContext):
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.finish()
	await message.reply('OK')


# Receive result start from page
async def start_page(message: types.Message, state: FSMContext):
	# process user input for starting page
	async with state.proxy() as data:
		data['start_page'] = str(message.text)
		await FSMadmin.next()
		await message.reply('Input last page')


# Receive result end page
async def stop_page(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['stop_page'] = str(message.text)
		await sqlite.sql_add(state)
		await state.finish()


# Register handlers
def register_handlers_admin(dp: Dispatcher):
	dp.register_message_handler(cm_start, state=None)
	dp.register_message_handler(cancel_handler, state="*", commands="cancel")
	dp.register_message_handler(start_page, state=FSMadmin.start_page)
	dp.register_message_handler(stop_page, state=FSMadmin.stop_page)

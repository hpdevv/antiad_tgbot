from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData
from vars import *
from main import dp
from inline.buttons import *

@dp.callback_query_handler(text="this_error_callback")
async def this_error(query: CallbackQuery):
	call_id = query.from_user.id
	if call_id != id:
		await query.answer("Для вас эта кнопка недоступна.")
		return
	if text == 0:
		await query.answer("Срок действия данной кнопки истёк.")
		return
	global used
	if used == 0:
		inline = InlineKeyboardMarkup()
		inline.add(InlineKeyboardButton(text="Да, это реклама.", callback_data="eto_reklama"))
		inline.add(InlineKeyboardButton(text="Нет, это не реклама.", callback_data="eto_ne_reklama"))
		await query.answer("Запрос отправлен.")
		await bot.send_message(hpdev_id, f"Пришло сообщение на проверку.\n\n{text}\n\nЭто реклама или оскорбление?", reply_markup=inline)
		used = 1
	else:
		await query.answer("Кнопка уже активирована.")
	
@dp.callback_query_handler(text="eto_reklama")
async def eto_reclama(query: CallbackQuery):
	global use
	if use == 0:
		use = 1
		await bot.send_message(id, "Пришёл ответ, это не ошибка. Просим вас не отправлять запросы о ошибке намеренно.")
	else:
		await query.answer("Кнопка уже активирована.")
	
@dp.callback_query_handler(text="eto_ne_reklama")
async def eto_ne_reclama(query: CallbackQuery):
	global useds
	if useds == 0:
		await bot.restrict_chat_member(chat_id, id, types.ChatPermissions(True))
		useds = 1
		await bot.send_message(id, "Пришёл ответ, это ошибка. Вы были размучены. Просим прощения за неудобство.")
	else:
		await query.answer("Кнопка уже активирована.")
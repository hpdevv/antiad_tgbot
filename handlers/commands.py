from aiogram import Bot, Dispatcher, types
from datetime import datetime, timedelta
from vars import *
from database.database import *
import inline.callbacks
from inline.buttons import *
from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData
from inline.buttons import *

async def start_command(message: types.Message):
	await message.reply("Привет! Я бот проверки на рекламу для чатов на основе ИИ GPT-3.5-Turbo. Просто введи /report отвечая на сообщение и всё!")

async def report_command(message: types.Message):
	message_log = [
	{"role": "system", "content": "You are a helpful assistant."}
	]
	if message.reply_to_message:
		try:
			replied_message_text = message.reply_to_message.text
			if replied_message_text == "реклама" or replied_message_text == "Реклама"  or replied_message_text == "Не реклама" or replied_message_text == "не реклама":
				await message.reply_to_message.reply("Не реклама")
				pass
			else:
				top = replied_message_text + "  это реклама? просто ответь да или нет, так же все ссылки это реклама."
				message_log.append({"role": "user", "content": top})
				response = send_message(message_log)
				message_log.append({"role": "assistant", "content": response})
				print(f"AI response: {response}")
				#with open("ad_log.txt", 'a') as f:
					#f.write(f"{replied_message_text}:\n    {response}\n\n")
				response = 0
				message_log.append({"role": "user", "content": top})
				response = send_message(message_log)
				message_log.append({"role": "assistant", "content": response})
				if "Да" in response:
					dt = datetime.now() + timedelta(minutes=60)
					timestamp = dt.timestamp()
					#await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
					global chat_id
					chat_id = message.chat.id
					inline = InlineKeyboardMarkup()
					inline.add(InlineKeyboardButton(text="Ошибка", callback_data="this_error_callback"))
					await message.reply(f"{message.reply_to_message.from_user.first_name} получает мут на 1 час за рекламу. Если это ошибка нажмите кнопку ниже.", reply_markup=inline)
					global text
					text = replied_message_text
					global id
					id = message.reply_to_message.from_user.id
					cursor.execute('INSERT INTO messages (text, answer, username, gpt_ver) VALUES (?, ?, ?, ?)', (text, response, message.reply_to_message.from_user.username, gpt_vers))
					conn.commit()
					#conn.close()
					#print(f"тру: {text}")
					await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
					response = 0
					return
				else:
					await message.reply_to_message.reply("Не реклама")
					cursor.execute('INSERT INTO messages (text, answer, username, gpt_ver) VALUES (?, ?, ?, ?)', (text, response, message.reply_to_message.from_user.username, gpt_vers))
					conn.commit()
					response = 0
					return
					
		except:
			replied_message_text = message.reply_to_message.text
			if replied_message_text == "реклама" or replied_message_text == "Реклама"  or replied_message_text == "Не реклама" or replied_message_text == "не реклама":
				await message.reply_to_message.reply("Не реклама")
				pass
			else:
				#await message.answer("Сервер перегружен... Подождите 20 секунд.")
				#sleep(20.0)
				#replied_message = message.reply_to_message
        		#await message.answer(f"Текст сообщения, на которое отвечают: {replied_message_text}")
				top = replied_message_text + "  это реклама? просто ответь да или нет, так же все ссылки это реклама."
				message_log.append({"role": "user", "content": top})
				response = send_message(message_log)
				message_log.append({"role": "assistant", "content": response})
				print(f"AI response: {response}")
				#with open("ad_log.txt", 'a') as f:
					#f.write(f"{replied_message_text}:\n    {response}\n\n")
				response = 0
				message_log.append({"role": "user", "content": top})
				response = send_message(message_log)
				message_log.append({"role": "assistant", "content": response})
				if "Да" in response:
					dt = datetime.now() + timedelta(minutes=60)
					timestamp = dt.timestamp()
					#await bot.restrict_chat_member(message.chat.id, message.reply_to_message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
					chat_id = message.chat.id
					inline = InlineKeyboardMarkup()
					inline.add(InlineKeyboardButton(text="Ошибка", callback_data="this_error_callback"))
					await message.reply(f"{message.reply_to_message.from_user.first_name} получает мут на 1 час за рекламу. Если это ошибка нажмите кнопку ниже.", reply_markup=inline)
					text = replied_message_text
					id = message.reply_to_message.from_user.id
					cursor.execute('INSERT INTO messages (text, answer, username, gpt_ver) VALUES (?, ?, ?, ?)', (text, response, message.reply_to_message.from_user.username, gpt_vers))
					conn.commit()
					#conn.close()
					#print(f"екскепт: {text}")
					await bot.delete_message(message.chat.id, message.reply_to_message.message_id)
					response = 0
					return
				else:
					await message.reply_to_message.reply("Не реклама")
					cursor.execute('INSERT INTO messages (text, answer, username, gpt_ver) VALUES (?, ?, ?, ?)', (text, response, message.reply_to_message.from_user.username, gpt_vers))
					conn.commit()
					response = 0
					return
		return
	else:
		await message.answer("Вы не ответили на сообщение")

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
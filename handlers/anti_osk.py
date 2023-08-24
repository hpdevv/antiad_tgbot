from aiogram import Bot, Dispatcher, types
from vars import *

async def check_na_osk(message: types.Message):
	message_text = message.text
	if message.text.lower() in anti_osk:
		print("оск")
		message_log = [
		{"role": "system", "content": "You are a helpful assistant."}
		]
		answer_to_gpt = message_text + "  это оскорбление? просто ответь да или нет."
		message_log.append({"role": "user", "content": answer_to_gpt})
		response = send_message(message_log)
		message_log.append({"role": "assistant", "content": response})
		print(f"АИ РЕСПОНС: {response}")
		if "Да" in response:
			dt = datetime.now() + timedelta(minutes=60)
			timestamp = dt.timestamp()
			await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
			global chat_id
			chat_id = message.chat.id
			inline = InlineKeyboardMarkup()
			inline.add(InlineKeyboardButton(text="Ошибка", callback_data="this_error_callback"))
			await message.reply(f"{message.from_user.first_name} получает мут на 1 час за оскорбления. Если это ошибка нажмите кнопку ниже.", reply_markup=inline)
			global text
			text = message.text
			global id
			id = message.from_user.id
			cursor.execute('INSERT INTO messages (text, answer, username, gpt_ver) VALUES (?, ?, ?, ?)', (text, response, message.from_user.username, gpt_vers))
			conn.commit()
			#conn.close()
			#print(f"тру: {text}")
			await bot.delete_message(message.chat.id, message.message_id)
			response = 0
			return
		else:
			response = 0
			answer_to_gpt = message_text + "  это оскорбление?"
			message_log.append({"role": "user", "content": answer_to_gpt})
			response = send_message(message_log)
			message_log.append({"role": "assistant", "content": response})
			if "Да" in response:
				dt = datetime.now() + timedelta(minutes=60)
				timestamp = dt.timestamp()
				await bot.restrict_chat_member(message.chat.id, message.from_user.id, types.ChatPermissions(False), until_date = timestamp)
				chat_id = message.chat.id
				inline = InlineKeyboardMarkup()
				inline.add(InlineKeyboardButton(text="Ошибка", callback_data="this_error_callback"))
				await message.reply(f"{message.from_user.first_name} получает мут на 1 час за оскорбления. Если это ошибка нажмите кнопку ниже.", reply_markup=inline)
				text = message.text
				id = message.from_user.id
				cursor.execute('INSERT INTO messages (text, answer, username, gpt_ver) VALUES (?, ?, ?, ?)', (text, response, message.from_user.username, gpt_vers))
				conn.commit()
				#conn.close()
				#print(f"тру: {text}")
				await bot.delete_message(message.chat.id, message.message_id)
				response = 0
				return
			else:
				return
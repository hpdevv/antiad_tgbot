'''
    Для работы бота эти переменные необходимы.
'''
import openai
import configparser
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

config = configparser.ConfigParser()
config.read("settings.ini")
bot_token = config["settings"]["token"]
api_key = config["settings"]["openai_key"]

openai.api_key = api_key

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

anti_osk = ['мать ебал', 'канаву', 'безмамный', 'шлюха', 'безмамная', 'шалава', 'ебал', 'ебут', 'нахуй', 'ебало', 'хуесос', 'даун', 'ебанулся', 'еблан', 'ебучий', 'ебаный', 'ебанный', 'долбаёб', 'долбаеб', 'далбаёб', 'далбаеб', 'ебанутый', 'ебаннутый', 'ёбнутый', 'шлюху', 'пидар', 'пидор', 'пидорас', 'пидарас', 'на хуй', 'шалавы', 'от хуя', 'отхуя', 'ебашут', 'лох', 'ебобо', 'баран', 'пизда']
response = 0
text = 0
id = 0
hpdev_id = 988195055
chat_id = 0
used = 0
use = 0
useds = 0
gpt_vers = "GPT-3.5-Turbo"

def send_message(message_log):
    global response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_log,
        max_tokens=2000,
        stop=None,
        temperature=0.7,
    )

    for choice in response.choices:
        if "text" in choice:
            return choice.text
            
    return response.choices[0].message.content

def setgpt(message_log):
	response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message_log,
        max_tokens=2048,
        stop=None,
        temperature=0.7,
    )
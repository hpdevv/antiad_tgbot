from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .callbacks import *
from handlers.commands import *

inline = InlineKeyboardMarkup()
inline.add(InlineKeyboardButton(text="Ошибка", callback_data="this_error_callback"))
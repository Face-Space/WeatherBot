from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

answer_kb = InlineKeyboardBuilder()
answer_kb.add(InlineKeyboardButton(text="Да", callback_data="yes"))
answer_kb.add(InlineKeyboardButton(text="Нет", callback_data="no"))
answer_kb.adjust(2)



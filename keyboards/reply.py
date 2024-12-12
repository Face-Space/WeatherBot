from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Перезапуск"),
        KeyboardButton(text="Уведомления"),
    ],
    [
        KeyboardButton(text="Отправить свою геопозицию", request_location=True)
    ],

], resize_keyboard=True, input_field_placeholder="Что Вас интересует?")


# start_kb2 = ReplyKeyboardBuilder()  # если использовать этот билдер, тогда надо записать в reply_markup=
# # =reply.start_kb2.as_markup(resize_keyboard=True, input_field_placeholder="Что Вас интересует?")
# start_kb2.add(
#     KeyboardButton(text="Перезапуск"),
#     KeyboardButton(text="Уведомления"),
#     KeyboardButton(text="Отправить локацию", request_location=True)
# )
# start_kb2.adjust(2)


# test_kb = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="Отправить локацию", request_location=True)
#         ]
# ])




from aiogram.utils.keyboard import KeyboardButton, ReplyKeyboardMarkup

KB_START = ReplyKeyboardMarkup(
    resize_keyboard=True, keyboard=[[KeyboardButton(text="Help")]]
)

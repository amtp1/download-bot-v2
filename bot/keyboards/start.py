from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

KB_START = ReplyKeyboardMarkup(
    resize_keyboard=True, keyboard=[
        [KeyboardButton(text="Help")]
    ]
)

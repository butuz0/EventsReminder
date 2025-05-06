from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

USERNAME_VERIFY_BUTTON = 'Верифікація через username'
PHONE_NUMBER_VERIFY_BUTTON = 'Верифікація через номер телефону'


verification_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=USERNAME_VERIFY_BUTTON)],
        [KeyboardButton(text=PHONE_NUMBER_VERIFY_BUTTON, request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

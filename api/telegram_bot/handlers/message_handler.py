from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from apps.profiles.models import TelegramData
from .states import AuthStates
from .messages.registration import MESSAGES, user_not_found

router = Router()


@sync_to_async(thread_sensitive=True)
def get_user_by_username(username) -> TelegramData | None:
    return TelegramData.objects.filter(telegram_username=username).first()


@sync_to_async(thread_sensitive=True)
def get_user_by_phone(phone_number) -> TelegramData | None:
    return TelegramData.objects.filter(telegram_phone_number=phone_number).first()


@sync_to_async(thread_sensitive=True)
def save_user(user: TelegramData, chat_id: int, user_id: int, username: str = None) -> None:
    user.telegram_chat_id = chat_id
    user.telegram_user_id = user_id
    user.is_verified = True
    
    if username is not None:
        user.telegram_username = username

    user.save()


@router.message(F.text, Command("start"))
async def any_message(message: Message):
    await message.reply(MESSAGES['start'])


@router.message(F.text)
async def handle_message(message: Message, state: FSMContext):
    username = message.from_user.username
    if not username:
        await message.reply(MESSAGES['no_username'])
        return

    user = await get_user_by_username(username)

    if user:
        await save_user(user, message.chat.id, message.from_user.id)
        await message.reply(MESSAGES['verification_successful'])
    else:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text='Надати номер телефону', request_contact=True)]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        await message.reply(MESSAGES['ask_phone'], reply_markup=keyboard)
        await state.set_state(AuthStates.waiting_for_phone)


@router.message(F.contact, AuthStates.waiting_for_phone)
async def handle_phone(message: Message, state: FSMContext):
    if not message.contact:
        await message.reply(MESSAGES['ask_phone'])
        return

    phone_number = message.contact.phone_number
    user = await get_user_by_phone(phone_number)

    if user:
        await save_user(user, message.chat.id, message.from_user.id, message.from_user.username)
        await message.reply(MESSAGES['verification_successful'])
    else:
        await message.reply(user_not_found(username=message.from_user.username))

    await state.clear()

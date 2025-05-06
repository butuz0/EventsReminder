from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from asgiref.sync import sync_to_async
from apps.profiles.models import TelegramData
from .states import VerificationStates
from telegram_bot.messages.verification import MESSAGES, user_not_found
from telegram_bot.keyboards.verification import USERNAME_VERIFY_BUTTON

router = Router()


@sync_to_async(thread_sensitive=True)
def get_user_by_username(username: str) -> TelegramData | None:
    return TelegramData.objects.filter(telegram_username=username).first()


@sync_to_async(thread_sensitive=True)
def get_user_by_phone(phone: str) -> TelegramData | None:
    return TelegramData.objects.filter(telegram_phone_number=phone).first()


@sync_to_async(thread_sensitive=True)
def save_user(user: str, chat_id: int, user_id: int, username: str = None) -> None:
    user.telegram_chat_id = chat_id
    user.telegram_user_id = user_id
    user.is_verified = True
    
    if username:
        user.telegram_username = username
        
    user.save()


@router.message(F.text == USERNAME_VERIFY_BUTTON, VerificationStates.unverified)
async def verify_by_username(message: Message, state: FSMContext):
    username = message.from_user.username
    if not username:
        await message.reply(MESSAGES['no_username'])
        return

    user = await get_user_by_username(username)
    if user:
        await save_user(user, message.chat.id, message.from_user.id)
        await state.set_state(VerificationStates.verified)
        await message.reply(MESSAGES['verification_successful'], 
                            reply_markup=ReplyKeyboardRemove())
    else:
        await message.reply(user_not_found(username=username))


@router.message(F.contact, VerificationStates.unverified)
async def verify_by_phone_number(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    
    if not phone.startswith('+'):
        phone = '+' + phone
    
    user = await get_user_by_phone(phone)
    if user:
        await save_user(user, message.chat.id, message.from_user.id, message.from_user.username)
        await state.set_state(VerificationStates.verified)
        await message.reply(MESSAGES['verification_successful'], 
                            reply_markup=ReplyKeyboardRemove())
    else:
        await message.reply(user_not_found(phone=phone))

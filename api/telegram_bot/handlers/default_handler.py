from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from .states import VerificationStates
from telegram_bot.messages.verification import MESSAGES

router = Router()


@router.message(F.text)
async def handle_message(message: Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == VerificationStates.verified:
        await message.reply(MESSAGES['already_verified'])
    else:
        await message.reply(MESSAGES['ask_verification'])
        await state.set_state(VerificationStates.unverified)

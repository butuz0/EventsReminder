from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from telegram_bot.messages.verification import MESSAGES
from telegram_bot.keyboards.verification import verification_keyboard
from .states import VerificationStates

router = Router()


@router.message(Command('start'))
async def start_command(message: Message, state: FSMContext):
    await state.set_state(VerificationStates.unverified)
    await message.reply(MESSAGES['start'], 
                        reply_markup=verification_keyboard)

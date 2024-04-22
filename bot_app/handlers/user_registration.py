from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot_app.core.constants import Messages, LoggingSettings
from bot_app.keyboards.reply import (
    REGISTER_KBRD,
    MAIN_MENU_ACTIVE_KBRD,
    CANCEL_KBRD
)
from bot_app.database.models import User
from bot_app.handlers.constants import UserRegistration, Texts


logger.add(LoggingSettings.FILE_NAME,
           rotation=LoggingSettings.ROTATION,
           backtrace=True,
           diagnose=True)
user_reg_router = Router()


class AddUser(StatesGroup):
    name = State()
    last_name = State()
    email = State()

    texts = {
        'AddUser:name': Texts.ENTER_NAME,
        'AddUser:last_name': Texts.ENTER_LAST_NAME,
        'AddUser:mail': Texts.ENTER_EMAIL,
    }


@user_reg_router.message(StateFilter(None),
                         F.text == UserRegistration.REGISTER)
async def add_name(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    """Start of user registration."""
    try:
        if await User.get(session, int(message.from_user.id)):
            await message.answer(
                UserRegistration.CANT_REGISTER,
                reply_markup=MAIN_MENU_ACTIVE_KBRD
            )
            await state.clear()
            return
        else:
            await message.answer(
                UserRegistration.ADD_NAME,
                reply_markup=CANCEL_KBRD
            )
            await state.set_state(AddUser.name)
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in add_name function: {e}")


@user_reg_router.message(StateFilter('*'), Command(UserRegistration.CANCEL))
@user_reg_router.message(StateFilter('*'),
                         F.text.casefold() == UserRegistration.CANCEL)
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    """Cancels all registration actions."""
    try:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.clear()
        await message.answer(
            UserRegistration.CANCSEL_MSG,
            reply_markup=REGISTER_KBRD
        )
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in cancel_handler function: {e}")


@user_reg_router.message(StateFilter('*'), Command(UserRegistration.BACK))
@user_reg_router.message(StateFilter('*'),
                         F.text.casefold() == UserRegistration.BACK)
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    """Step back to register."""
    try:
        current_state = await state.get_state()
        if current_state == AddUser.name:
            await message.answer(UserRegistration.NO_STEP)
            return
        previous = None
        for step in AddUser.__all_states__:
            if step.state == current_state:
                await state.set_state(previous)
                await message.answer(
                    f'{UserRegistration.PREVIOUS_STEP.value}\n'
                    f'{AddUser.texts[previous.state]}'
                )
                return
            previous = step
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in back_step_handler function: {e}")


@user_reg_router.message(AddUser.name, F.text)
async def add_last_name(message: types.Message, state: FSMContext):
    """Adding last name."""
    try:
        name = message.text
        if check_alpha(name):
            await state.update_data(name=name)
            await message.answer(UserRegistration.ADD_LAST_NAME)
            await state.set_state(AddUser.last_name)
        else:
            await message.answer(UserRegistration.NAME_RULES)
            await state.set_state(AddUser.name)
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in add_last_name function: {e}")


@user_reg_router.message(AddUser.last_name, F.text)
async def add_mail(message: types.Message, state: FSMContext):
    """Adding mail."""
    try:
        last_name = message.text
        if check_alpha(last_name):
            await state.update_data(last_name=last_name)
            await message.answer(UserRegistration.ADD_EMAIL)
            await state.set_state(AddUser.email)
        else:
            await message.answer(UserRegistration.LAST_NAME_RULES)
            await state.set_state(AddUser.last_name)
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in add_mail function: {e}")


@user_reg_router.message(AddUser.email,
                         F.text.contains(UserRegistration.EMAIL_DOMAIN))
async def refister(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    """End of registration."""
    try:
        tg_user = await User.get_by_email(session, message.text.lower())
        if tg_user is not None:
            await message.answer(UserRegistration.EMAIL_EXIST)
        else:
            await state.update_data(email=message.text.lower())
            data = await state.get_data()
            data['tg_id'] = message.from_user.id
            await User.create(session, data)
            await state.clear()
            await message.answer(
                UserRegistration.COMPLITE_MSG,
                reply_markup=MAIN_MENU_ACTIVE_KBRD
            )
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in refister function: {e}")


@user_reg_router.message(AddUser.email)
async def invalid_mail(message: types.Message, state: FSMContext):
    """Report about incorrect mail."""
    try:
        await message.answer(UserRegistration.INVALID_EMAIL)
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in invalid_mail function: {e}")


def check_alpha(input_string):
    """Checking all symbols are letters."""
    try:
        return all(char.isalpha() or char.isspace() for char in input_string)
    except Exception as e:
        logger.error(f"Error in check_alpha function: {e}")

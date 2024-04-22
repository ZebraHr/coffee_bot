"""Telegram bot administration."""
from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot_app.core.constants import Messages, LoggingSettings
from bot_app.database.models import User
from bot_app.filters.is_admin import IsAdmin
from bot_app.handlers.constants import AdminConsts
from bot_app.keyboards.reply import ADMIN_KBRD, CANCEL_ONLY_KBRD
from bot_app.handlers.user_registration import user_reg_router


logger.add(LoggingSettings.FILE_NAME,
           rotation=LoggingSettings.ROTATION,
           backtrace=True,
           diagnose=True)
admin_router = Router()


class DelUser(StatesGroup):
    email = State()


class DeactiveUser(StatesGroup):
    email = State()


class AddUserToAdmin(StatesGroup):
    email = State()
    rem_email = State()


@admin_router.message(StateFilter(None), Command('admin'), IsAdmin())
async def get_admin_commands(message: types.Message):
    """Getting admin keyboard."""
    try:
        await message.answer(AdminConsts.ADMIN_ONLY, reply_markup=ADMIN_KBRD)
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in get_admin_commands function: {e}")


@admin_router.message(F.text == AdminConsts.ALL_USERS, IsAdmin())
async def get_user_list(message: types.Message, session: AsyncSession):
    """Getting list of all users."""
    try:
        user_list_str = '\n'.join(
            repr(user) for user in await User.get_all(session)
        )
        if user_list_str:
            await message.answer(user_list_str)
        else:
            await message.answer(AdminConsts.NOT_FOUND)
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in get_user_list function: {e}")


@admin_router.message(StateFilter(None),
                      F.text == AdminConsts.DELETE_USER, IsAdmin())
async def delete_user(message: types.Message, state: FSMContext):
    """Deleting user. Waiting for user email."""
    try:
        await message.answer(
            AdminConsts.ADD_EMAIL,
            reply_markup=CANCEL_ONLY_KBRD
        )
        await state.set_state(DelUser.email)
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in delete_user function: {e}")


@admin_router.message(DelUser.email, F.text)
async def delete_user_id(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    """Removing user by email."""
    try:
        await state.update_data(email=message.text.lower())
        tg_user = await User.get_by_email(session, message.text.lower())
        if tg_user is not None:
            if await User.remove(session, tg_user):
                await message.answer(
                    AdminConsts.DELETE_COMPLITE,
                    reply_markup=ADMIN_KBRD
                )
                await state.clear()
        else:
            await message.answer(
                AdminConsts.NOT_FOUND, reply_markup=ADMIN_KBRD)
            await state.clear()
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in delete_user_id function: {e}")


@admin_router.message(StateFilter(None),
                      F.text == AdminConsts.DEACTIVATE_USER, IsAdmin())
async def deactive_user(message: types.Message, state: FSMContext):
    """Deactivating user. Waiting for user email."""
    try:
        await message.answer(
            AdminConsts.ADD_EMAIL,
            reply_markup=CANCEL_ONLY_KBRD
        )
        await state.set_state(DeactiveUser.email)
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in deactive_user function: {e}")


@admin_router.message(DeactiveUser.email, F.text)
async def deactivate_user_id(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    """Deactivating user by email."""
    try:
        await state.update_data(email=message.text.lower())
        deactive = await User.deactivate_user(session, message.text.lower())
        if deactive:
            await message.answer(
                AdminConsts.DEACTIVATE_COMPLITE,
                reply_markup=ADMIN_KBRD
            )
            await state.clear()
        else:
            await message.answer(AdminConsts.NOT_FOUND,
                                 reply_markup=ADMIN_KBRD)
            await state.clear()
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in deactivate_user_id function: {e}")


@admin_router.message(F.text == AdminConsts.ADD_USER_TO_ADMIN, IsAdmin())
async def add_user_to_admin(message: types.Message, state: FSMContext):
    """Adding user to admins."""
    try:
        await state.update_data(email=message.text.lower())
        await message.answer(AdminConsts.ADD_EMAIL,
                             reply_markup=CANCEL_ONLY_KBRD)
        await state.set_state(AddUserToAdmin.email)
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in add_user_to_admin function: {e}")


@admin_router.message(StateFilter(None),
                      F.text == AdminConsts.REMOVE_USER_FROM_ADMIN, IsAdmin())
async def remove_user_from_admin(message: types.Message, state: FSMContext):
    """Deleting user from admins. Waiting for user email."""
    try:
        await state.update_data(email=message.text.lower())
        await message.answer(AdminConsts.ADD_EMAIL,
                             reply_markup=CANCEL_ONLY_KBRD)
        await state.set_state(AddUserToAdmin.rem_email)
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in remove_user_from_admin function: {e}")


@admin_router.message(AddUserToAdmin.email)
async def add_to_admin(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    """Adding user to admins by email."""
    try:
        result = await session.execute(
            select(User).filter(User.email == message.text.lower())
        )
        user = result.scalars().one_or_none()
        if user:
            if user.is_admin:
                await message.answer(AdminConsts.ADMIN_ALREADY,
                                     reply_markup=ADMIN_KBRD)
            else:
                user.is_admin = True
                await session.commit()
                await message.answer(AdminConsts.SUCCESS,
                                     reply_markup=ADMIN_KBRD)
                await state.clear()
        else:
            await message.answer(AdminConsts.NOT_FOUND,
                                 reply_markup=ADMIN_KBRD)
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in add_to_admin function: {e}")


@admin_router.message(AddUserToAdmin.rem_email)
async def remove_from_admin(
    message: types.Message,
    state: FSMContext,
    session: AsyncSession
):
    """Removing user from admins by email."""
    try:
        result = await session.execute(
            select(User).filter(User.email == message.text.lower())
        )
        user = result.scalars().one_or_none()
        if user:
            if user.is_admin:
                user.is_admin = False
                await session.commit()
                await message.answer(AdminConsts.ANTI_SUCCESS,
                                     reply_markup=ADMIN_KBRD)
                await state.clear()
            else:
                await message.answer(AdminConsts.NON_USER_ADMIN,
                                     reply_markup=ADMIN_KBRD)
                await state.clear()
        else:
            await message.answer(AdminConsts.NOT_FOUND,
                                 reply_markup=ADMIN_KBRD)
            await state.clear()
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in remove_from_admin function: {e}")


@user_reg_router.message(StateFilter('*'),
                         Command(AdminConsts.CANCEL_ADMIN), IsAdmin())
@user_reg_router.message(StateFilter('*'),
                         F.text.casefold() == AdminConsts.CANCEL_ADMIN,
                         IsAdmin())
async def cancel_actions_handler(
    message: types.Message, state: FSMContext
) -> None:
    """Cancels admin actions."""
    try:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.clear()
        await message.answer(AdminConsts.CANCSEL_MSG, reply_markup=ADMIN_KBRD)
    except Exception as e:
        await message.answer(Messages.ERROR_MSG_FOR_USER)
        logger.error(f"Error in cancel_handler function: {e}")

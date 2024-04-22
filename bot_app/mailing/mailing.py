from typing import List, Optional, Tuple

from aiogram.types.inline_keyboard_button import InlineKeyboardButton
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot_app.core.config import bot, settings
from bot_app.core.constants import LoggingSettings
from bot_app.database.models import User
from bot_app.mailing.distribution import distribute_pairs
from bot_app.mailing.constants import Mailing


logger.add(LoggingSettings.FILE_NAME,
           rotation=LoggingSettings.ROTATION,
           backtrace=True,
           diagnose=True)


meet_inline_buttons = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=Mailing.MEET_OK,
                              callback_data=Mailing.BUTTON_MEETING),
         InlineKeyboardButton(text=Mailing.MEET_FALSE,
                              callback_data=Mailing.BUTTON_MEETING)],
        [InlineKeyboardButton(text=Mailing.MEET_END_OF_WEEK,
                              callback_data=Mailing.BUTTON_MEETING)],
    ])


async def mailing_by_user_tg_id(
    chat_id: str,
    text: str,
    inline_buttons: Optional[InlineKeyboardMarkup] = None
):
    """Mailing by tg_id."""
    await bot.send_message(chat_id=chat_id, text=text,
                           reply_markup=inline_buttons)


async def meeting_mailing(
    session: AsyncSession,
    meetings_pairs: List[Tuple[User, User]] = None
):
    """Mailing to pairs."""
    for pair in meetings_pairs:
        await mailing_by_user_tg_id(
            chat_id=pair[0].tg_id,
            text=Mailing.MEETING_MESSAGE.format(
                pair[1].name, pair[1].last_name, pair[1].email
            ))
        await mailing_by_user_tg_id(
            chat_id=pair[1].tg_id,
            text=Mailing.MEETING_MESSAGE.format(
                pair[0].name, pair[0].last_name, pair[0].email
            ))
        await User.set_is_sent_status_true(pair, session)
        logger.info(
            f'Send meeting message to users {pair[0].name} and {pair[1].name}'
        )


async def meeting_reminder_mailing(session: AsyncSession):
    """Remainder mailing."""
    users = await User.get_all_is_sent(session)
    for user in users:
        await mailing_by_user_tg_id(
            chat_id=user.tg_id,
            text=Mailing.REMINDER_MAILING,
            inline_buttons=meet_inline_buttons
        )
        logger.info(f'Send reminder message to user {user.name}')
    await User.set_is_sent_status_false(users, session)


async def newsletter_about_the_meeting(session: AsyncSession):
    """Mailing about meetings."""
    data = await distribute_pairs(session)
    if data.get('pairs') is not None:
        await meeting_mailing(session, data['pairs'])
    else:
        await bot.send_message(chat_id=settings.gen_admin_id,
                               text=Mailing.NO_ACTIVE)
        logger.info(
            f'Send warning message to genadmin id {settings.gen_admin_id}'
        )
    if data.get('no_pair') is not None:
        await mailing_by_user_tg_id(
            chat_id=data['no_pair'].tg_id, text=Mailing.TEXT_NO_PAIR
        )
        logger.info(f'Send sorry message to user {data["no_pair"].name}')

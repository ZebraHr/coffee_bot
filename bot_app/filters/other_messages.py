from aiogram import types
from aiogram.filters import Filter

from bot_app.handlers.constants import (AdminConsts,
                                        BaseCommands,
                                        UserRegistration, Texts)
from bot_app.keyboards.constants import (MainMenuKbrd,
                                         AdminKbrd, Register,
                                         NextMoreKbrd, CancelKbrd, OnlyKbrd)
from bot_app.mailing.constants import Mailing


class OtherMsgsFilter(Filter):
    """Filter for garbage messages."""

    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message) -> bool:
        if message.text.startswith('/'):
            return False

        if message.text in [item for item in AdminConsts] \
                or message.text in [item for item in BaseCommands] \
                or message.text in [item for item in UserRegistration] \
                or message.text in [item for item in Texts] \
                or message.text in [item for item in MainMenuKbrd] \
                or message.text in [item for item in AdminKbrd] \
                or message.text in [item for item in Register] \
                or message.text in [item for item in NextMoreKbrd] \
                or message.text in [item for item in CancelKbrd] \
                or message.text in [item for item in OnlyKbrd] \
                or message.text == Mailing.MEET_OK \
                or message.text == Mailing.MEET_FALSE \
                or message.text == Mailing.MEET_END_OF_WEEK:
            return False

        return True

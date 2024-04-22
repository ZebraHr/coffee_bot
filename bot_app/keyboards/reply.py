"""Application keyboard"""
from typing import List

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot_app.keyboards.constants import (
    AdminKbrd,
    Register,
    NextMoreKbrd,
    CancelKbrd,
    OnlyKbrd,
    MainMenuKbrd
)


def get_keyboard(
    *btns: str,
    placeholder: str = None,
    request_contact: int = None,
    request_location: int = None,
    sizes: List[int] = [2],
):
    '''
    Parameters request_contact and request_location must be as indexes
    of btns args for buttons you need.
    Example:
    get_keyboard(
            'About us',
            'Registration',
            'Pause communication',
            request_contact=4,
            sizes=[2, 2, 1]
        )
    '''
    keyboard = ReplyKeyboardBuilder()
    for index, text in enumerate(btns, start=0):
        if request_contact and request_contact == index:
            keyboard.add(KeyboardButton(text=text, request_contact=True))
        elif request_location and request_location == index:
            keyboard.add(KeyboardButton(text=text, request_location=True))
        else:
            keyboard.add(KeyboardButton(text=text))
    return keyboard.adjust(*sizes).as_markup(
            resize_keyboard=True, input_field_placeholder=placeholder)


MAIN_MENU_ACTIVE_KBRD = get_keyboard(
    MainMenuKbrd.ABOUT_PROJECT,
    MainMenuKbrd.OUR_COLLEAGUES,
    MainMenuKbrd.SUSPEND_PARTICIPATION,
    sizes=[1, 1, 1]
)

MAIN_MENU_DEACTIVE_KBRD = get_keyboard(
    MainMenuKbrd.ABOUT_PROJECT,
    MainMenuKbrd.OUR_COLLEAGUES,
    MainMenuKbrd.RENEW_PARTICIPATION,
    sizes=[1, 1, 1]
)

MAIN_MENU_NOREG_KBRD = get_keyboard(
    MainMenuKbrd.ABOUT_PROJECT,
    MainMenuKbrd.OUR_COLLEAGUES,
    Register.REGISTRATION,
    sizes=[1, 1, 1]
)


ADMIN_KBRD = get_keyboard(
    AdminKbrd.USER_LIST,
    AdminKbrd.DELETE_USER,
    AdminKbrd.DEACTIVATE_USER,
    AdminKbrd.MAIN_MENU,
    AdminKbrd.ADD_ADMIN,
    AdminKbrd.REMOVE_ADMIN,
    sizes=[2, 2]
)

REGISTER_KBRD = get_keyboard(Register.REGISTRATION)

NEXT_KBRD = get_keyboard(
    NextMoreKbrd.NEXT_COMMENT,
    NextMoreKbrd.BACK_TO_MAIN_MENU,
    sizes=[2, ]
)

MORE_KBRD = get_keyboard(
    NextMoreKbrd.ANOTHER_COMMENT,
    NextMoreKbrd.BACK_TO_MAIN_MENU,
    sizes=[2, ]
)

CANCEL_KBRD = get_keyboard(
    CancelKbrd.CANCELLATION,
    CancelKbrd.BACK,
    sizes=[2, ]
)

CANCEL_ONLY_KBRD = get_keyboard(
    OnlyKbrd.CANCEL,
    sizes=[1, ]
)

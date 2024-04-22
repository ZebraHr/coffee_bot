from enum import Enum


class MainMenuKbrd(str, Enum):
    ABOUT_PROJECT = 'О проекте',
    OUR_COLLEAGUES = 'Наши коллеги про проект «Кофе Bслепую»',
    SUSPEND_PARTICIPATION = 'Приостановить участие',
    RENEW_PARTICIPATION = 'Возобновить участие',

    def __str__(self) -> str:
        return str.__str__(self)


class AdminKbrd(str, Enum):
    USER_LIST = 'Список всех пользователей',
    DELETE_USER = 'Удалить пользователя',
    DEACTIVATE_USER = 'Деактивировать пользователя',
    MAIN_MENU = 'Главное меню',
    ADD_ADMIN = 'Добавить администратора',
    REMOVE_ADMIN = 'Удалить администратора',

    def __str__(self) -> str:
        return str.__str__(self)


class Register(str, Enum):
    REGISTRATION = 'Регистрация'

    def __str__(self) -> str:
        return str.__str__(self)


class NextMoreKbrd(str, Enum):
    NEXT_COMMENT = 'Следующий комментарий',
    BACK_TO_MAIN_MENU = 'Главное меню',
    ANOTHER_COMMENT = 'Ещё комментарий',

    def __str__(self) -> str:
        return str.__str__(self)


class CancelKbrd(str, Enum):
    CANCELLATION = 'Отмена',
    BACK = 'Назад',

    def __str__(self) -> str:
        return str.__str__(self)


class OnlyKbrd(str, Enum):
    CANCEL = 'Отменить',

    def __str__(self) -> str:
        return str.__str__(self)

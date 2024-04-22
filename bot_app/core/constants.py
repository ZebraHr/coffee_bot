from enum import Enum, IntEnum


class MailingInt(IntEnum):
    MAIL_TO_COUPLES_HOUR = 10
    MAIL_TO_COUPLES_MIN = 00
    REMIND_MAIL_HOUR = 10
    REMIND_MAIL_MIN = 00


class MailingStr(str, Enum):
    TRIGGER = 'cron'
    MAIL_TO_COUPLES_DAY = 'mon'
    REMIND_MAIL_DAY = 'thu'

    def __str__(self) -> str:
        return str.__str__(self)


class Timezone(str, Enum):
    TIMEZONE_MOSCOW = 'Europe/Moscow'

    def __str__(self) -> str:
        return str.__str__(self)


class Messages(str, Enum):
    START_UP_MSG = 'Бот запущен'
    SHUT_DOWN_MSG = 'Бот лег'
    ERROR_MSG_FOR_USER = 'Извините, я сломался :( Но меня уже чинят!'
    GARBAGE_MSG = 'Извините, я вас не понимаю. Воспользуйтесь кнопками меню.'

    def __str__(self) -> str:
        return str.__str__(self)


class Commands(str, Enum):
    BOT_RESTART = 'Перезапустить бота'
    ADMIN_PANEL = 'Панель администратора'

    def __str__(self) -> str:
        return str.__str__(self)


class LoggingSettings(str, Enum):
    FILE_NAME = 'logging.log'
    ROTATION = '30 MB'

    def __str__(self) -> str:
        return str.__str__(self)

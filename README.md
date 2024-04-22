# Проект random_coffee_bot

## Описание

### Телеграм-Бот для ЗАО "Groupe SEB" ###
С помощью бота для сотрудников компаннии раз в неделю в случайном порядке подбирается пара из коллег для офлайн или онлайн встречи с целью выпить вместе чашечку кофе или чая. В конце рабочей недели приходит напоминание о встрече. Бот только подбирает пару, о встрече сотрудники договариваются самостоятельно.

Функционал телеграм-бота:
- для пользователя: регистрация, рассылка с именем и контактными данными коллеги (корпоративная почта), возможность на время отписаться от рассылкии -  не участвовать в распределении пары (в случае отпуска, болезни и тп) 
- для администратора: просмотр списка всех пользователей, возможность удалить пользователя из проекта, добавить пользователя в администраторы, а так же удалить его оттуда, отключение пользователя от рассылки

## Технологии
[![Python](https://img.shields.io/badge/python-3.11-blue?logo=python)](https://www.python.org/)
[![aiogram](https://img.shields.io/badge/aiogram-3.4-blue)](https://docs.aiogram.dev/en/latest/)
[![aiosqlite](https://img.shields.io/badge/aiosqlite-blue)](https://pypi.org/project/aiosqlite/)
[![APScheduler](https://img.shields.io/badge/APScheduler-blue)](https://docs-python.ru/packages/modul-apscheduler-python/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-blue)](https://docs.sqlalchemy.org/en/20/)
[![alembic](https://img.shields.io/badge/alembic-blue)](https://alembic.sqlalchemy.org/en/latest/)
[![pydentic](https://img.shields.io/badge/pydentic-blue)](https://pydantic-docs.helpmanual.io/)


## Запуск проекта локально

Клонируйте репозиторий и перейдите в него:

```
git clone git@github.com:Studio-Yandex-Practicum/random_coffee_bot_anna.git
cd random_coffee_bot_anna
```

Создайте виртуальное окружение:
```
py -3.11 -m venv venv
```
Активируйте виртуальное окружение:
```
Windows: source venv/Scripts/activate
Linux/macOS: source venv/bin/activate
```
Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
В корне проекта создайте файл .env и поместите в него:
```
BOT_TOKEN='<токен вашего бота>'
DATABASE_URL='sqlite+aiosqlite:///./random_coffe_bot.db'
GEN_ADMIN_ID=<телеграмм id главного администратора>
```
Создайте базу данных, применив миграции (из корня проекта):
```
alembic upgrade head
```
Запустите бота (из корня проекта):
```
python bot.py
```
## Запуск проекта на сервере
Клонируйте репозиторий и перейдите в него:
```
git clone git@github.com:Studio-Yandex-Practicum/random_coffee_bot_anna.git
cd random_coffee_bot_anna
```
Создайте виртуальное окружение:
```
python3.11 -m venv venv
```
Активируйте виртуальное окружение:
```
source venv/bin/activate
```
Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
В корне проекта создайте файл .env и поместите в него:
```
BOT_TOKEN='<токен вашего бота>'
DATABASE_URL='sqlite+aiosqlite:///./random_coffe_bot.db'
GEN_ADMIN_ID=<телеграмм id главного администратора>
```
Создайте базу данных, применив миграции (из корня проекта):
```
alembic upgrade head
```
Создайте юнита для автоматического перезапуска бота при перезагрузке сервера:
```
nano file_name.service
```
Поместите в файл следующее:
```
[Unit]
Description=<описание вашего бота>
After=multy-user.target

[Service]
Type=simple
ExecStart=/<путь до репозитория проекта>/random_coffee_bot_anna/venv/bin/python3.11 /<путь до репозитория проекта>/random_coffee_bot_anna/bot.py
WorkingDirectory=/<путь до репозитория проекта>/random_coffee_bot_anna
Restart=always

[Install]
WantedBy=multi-user.target
```
Последовательно выполните следующие команды:
```
sudo cp file_name.service /etc/systemd/system
sudo systemctl enable file_name.service
sudo systemctl restart file_name.service
```
Для перезапуска бота на сервере используйте команду:
```
sudo systemctl restart file_name.service
```
Поменять дни и время рассылки можно в bot_app/core/constants.py
```
class MailingInt(IntEnum):
    MAIL_TO_COUPLES_HOUR = 10  - время рассылки для пар (часы)
    MAIL_TO_COUPLES_MIN = 00 - время рассылки для пар (минуты)
    REMIND_MAIL_HOUR = 10  - время рассылки напоминания (часы)
    REMIND_MAIL_MIN = 00  - время рассылки напоминания (минуты)


class MailingStr(str, Enum):
    TRIGGER = 'cron'
    MAIL_TO_COUPLES_DAY = 'mon' - день расслыки для пар (принимает значения от 0 до 6, или mon, tue, wed, thu, fri, sat, sun, можно задать сразу несколько дней)
    REMIND_MAIL_DAY = 'thu' - день расслыки с напоминанием (принимает значения от 0 до 6, или mon, tue, wed, thu, fri, sat, sun,  можно задать сразу несколько дней)
```


## Команда разработки

[Анна Победоносцева](https://github.com/ZebraHr) (тимлид команды)

[Светлана Шатунова](https://github.com/SvShatunova) (разработчик)

[Ольга Скрябина](https://github.com/ibonish) (разработчик)

[Татьяна Мусатова](https://github.com/Tatiana314) (разработчик)

[Никита Пискунов](https://github.com/Nikitkosss) (разработчик)

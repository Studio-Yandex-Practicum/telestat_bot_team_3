# telestat_bot_team_3

## Правило именования веток Git
### Вся наша работа проходит в ветке development, перед продакшном сольем в master

### Если вы работаете над разработкой новой фичи проекта, структура имени ветки должна быть такой :
```
feauture/имя_вашей_фичи
```

### Если вы работаете над исправлением багов проекта, структура имени ветки должна быть такой :
```
bugfix/исправляемый_баг
```

### Pull Requests
## После написания кода в своей ветке делаем pull request, тим лид принмает код на ревью, если замечения не выявлены - ветка сливается,
## если по коду есть нарекания - возвращается на доработку 

Telegram-Бот для маркетинговых исследований телеграм каналов (Telestat) | Команда Максима Соловьева



## Технологии и библиотеки

* [Python](https://www.python.org/)
* [SQLAlchemy](https://pypi.org/project/SQLAlchemy/)
* [Alembic](https://pypi.org/project/alembic/)
* [Asyncio](https://docs.python.org/3/library/asyncio.html)
* [Aiogoogle](https://aiogoogle.readthedocs.io/en/latest/)

## Установите и настройте систему контроля версий репозиториев GIT,
## создайте ключ для ssh сессий с GitHub выполните команду:

* [GIT](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git/)

```
git clone git@github.com:Studio-Yandex-Practicum/telestat_bot_team_3.git
```

## Настройка проекта и организация подключения к базе данных PostgresSQL.

### Создать рабочую директорию проекта по вашему пути на сервере, 
### ny_work_directory/
### Для настройки проекта необходимо установить:

* Python версии 3.11.4 или выше

### Выполнить следующие команды для конфигурации "virtual enviroments" OS Windows
### и устанавливаем все необходимые зависимости проекта:
### Внимание для OS Linux команды будут отличаться!

```
python -m venv venv
source venv/Scripts/activate
python -m pip install --uprade pip
pip install -r requirements.txt
```
### Настройка подключения SQLAlchemy и Alembic для взаимодействия с Postgres:

Необходимо выполнить команду инициализации работы Alembic из консоли
находясь в рабочей директории проекта
```
alembic init --template async alembic
```

### Создать в корневой директории проекта файл .env и заполнить в нём следующее:

```
DB_URI=postgresql+asyncpg://you_username:you_password@10.0.0.7/you_database_name
API_ID=12345678
API_HASH=9999aa9aa9a9999a99a999aa9a599a99
BOT_TOKEN=1234567890:AAAzz2z2zzzPzPPz1zVCz0zzfXz_Kzz1234
```
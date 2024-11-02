# ITLobbyMinon

## Описание
ITLobbyMinon — это телеграм-бот, разработанный для администрирования IT-сообществ, в частности для "IT Lobby Irkutsk". Бот поддерживает отправку приветственных сообщений новым участникам, управление кнопками и конфигурацию приветственного интерфейса.

## Требования
- **Python 3.12**
- **Docker** и **docker-compose** (если планируете использовать контейнеризацию)

## Настройка проекта

## 1. Клонируйте репозиторий
```bash
git clone <URL_TO_REPOSITORY>
cd ITLobbyMinon
```

## 2. Создайте виртуальное окружение и установите зависимости

### Для локальной разработки:

### Linux/MacOS 
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### Windows
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3. Настройте переменные окружения(не забудьте поменять на свои)
```bash
cp .env.example .env
```

## 4. Настройка базы данных
```bash
alembic upgrade head
```

## 5. Запустите бота

### Запуск бота локально
```bash
python3 main.py
```

### Через Docker
```bash
docker-compose up --build -d
```

### Структура проекта

```tree
ITLobbyMinon/
├── .env.example
├── .gitignore
├── .python-version
├── Dockerfile
├── LICENSE
├── README.md
├── alembic.ini
├── docker-compose.yml
├── requirements.txt
├── run.py
└── src
    ├── __init__.py
    ├── chemas.py
    ├── config.py
    ├── database
    │   ├── __init__.py
    │   ├── connection.py
    │   ├── migrations
    │   │   ├── README
    │   │   ├── env.py
    │   │   ├── script.py.mako
    │   │   └── versions
    │   │       ├── 115f628e1d03_settings_base_conf.py
    │   │       └── 364cfff3dd87_initial.py
    │   └── models
    │       ├── __init__.py
    │       ├── butons.py
    │       ├── settings.py
    │       └── user.py
    ├── handlers
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── join2group.py
    │   └── start.py
    ├── states
    │   ├── __init__.py
    │   └── admin.py
    └── utils
        ├── __init__.py
        ├── keyboards
        │   ├── __init__.py
        │   ├── admin.py
        │   └── join2group.py
        └── welcome_message.py

```

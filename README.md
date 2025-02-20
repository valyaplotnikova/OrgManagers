# Система управления и контроля бизнеса
## Описание
Backend-часть приложения разделена на два микросервиса:
- **user_team_service** отвечает за взаимодействие с пользователями, компаниями и организионной структурой, в т.ч. управление через админ-панель. Реализован основной CRUD для работы с объектами.
- **task_motivation_service** отвечает за работу с задачами, мотивациями, встречами
У каждого сервиса подключение к своей базе данных. Сервисы взаимодействуют через API

## Структура проекта
```plaintext
task_motivation_service/
├── .env
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── task_app/
    ├── main.py
    ├── core/
    ├── database/
    ├── dependencies/
    ├── exceptions/
    ├── models/
    ├── repositories/
    ├── routers/
    ├── schemas/
    └── services/

user_team_service/
├── .env
├── alembic.ini
├── Dockerfile
├── requirements.txt
└── user_app/
    ├── main.py
    ├── core/
    ├── database/
    ├── dependencies/
    ├── exceptions/
    ├── models/
    ├── repositories/
    ├── routers/
    ├── schemas/
    └── services/

tests/
├── fixtures/
├── test_task_motivation_service/
└── test_user_team_service/
```

## Установка

1. Клонируйте данный репозиторий к себе на локальную машину: git clone https://github.com/valyaplotnikova/OrgManager.git

2. В файлах .env.example подставьте свои переменные окружения и переименуйте файлы в .env

3. Запустите Docker   
Введите команду в терминале:    

Для Compose V1:

```
docker-compose up -d --build 
```
Для Compose V2:
```
docker compose up -d --build 
```
4. Сервисы готовы для использования:
Для работы с user_team_service - http://localhost:8001
Для работы с админ-панелью - http://localhost:8001/admin
Для работы с task_motivation_service - http://localhost:8002

Документация доступна на:
Для работы с user_team_service - http://localhost:8001/docs
Для работы с task_motivation_service - http://localhost:8002/docs

## Тестирование

Основной функционал покрыт тестами.      
Для запуска теста необходимо из корня проекта выполнить команду:
```
pytest
```
или для запуска тестов с подробной информацией:
```
pytest -v
```
## Локальный запуск для разработки

Для локального запуска конкретного микросервиса, необходимо открыть его как корневую директорию и создать в корне .env, пример лежит в файле env.example так же в корневой директории.
Для каждого сервиса необходимо создать виртуальное окружение
python -m venv .venv
Активация виртуальной среды для OC Linux
```bash
source .venv/bin/activate
```
Активация виртуальной среды для OC Windows
```bash
venv\Scripts\activate
```
Далее, нужно установить зависимости:
```bash
pip install -r requirements.txt
```
Теперь любой сервис сможет подключиться к базе данных и функционировать полноценно. 




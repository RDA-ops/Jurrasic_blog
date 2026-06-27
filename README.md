# Jurassic Blog & Community

## Установка
1. Клонируйте репозиторий
2. Создайте виртуальное окружение: `python -m venv venv`
3. Активируйте: `.venv\Scripts\activate` (Windows) или `source venv/bin/activate` (Linux/Mac)
4. Установите зависимости: `pip install -r requirements.txt`
5. Примените миграции: `python manage.py migrate`
6. Создайте суперпользователя: `python manage.py createsuperuser`
7. Запустите сервер: `python manage.py runserver`

## Интеграция с API
- На главной странице отображается случайный факт о динозаврах с dinoapi.fly.dev.

## Тесты
`python manage.py test`

## Скриншоты
(добавить скриншоты)

## Логирование
Логи сохраняются в `logs.log`.

## Celery
Запуск фоновых задач: `celery -A jurassic_blog worker --loglevel=info`

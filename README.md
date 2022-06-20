# Web project
Создан сервис - аналог StackOverFlow.

# Технологический Стек
1. Фреймворк верстки - bootstap4
2. Фреймворк web-приложений - django
3. БД - SQLite

# Package Version
Список необходимых пакетов лежит в packages.txt

# Запуск
Создаем окружение
```c
python3 -m venv venv
```
Активируем
```c
source venv/bin/activate 
```
Создаем миграции
```c
python manage.py makemigrations
```
Создаем базу
```c
python manage.py migrate
```
Запускаем генератор данных БД
```c
python manage.py generate_data
```
Запускаем сервер
```c
python manage.py runserver
```
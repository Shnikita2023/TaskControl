# Cистема контроля заданий на выпуск продукции

[![Build status](https://github.com/Shnikita2023/taskcontrol/actions/workflows/delpoyment.yml/badge.svg?branch=main)](https://github.com/Shnikita2023/taskcontrol/actions/workflows/delpoyment.yml)


[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?style=flat-square&logo=Alembic)](https://alembic.sqlalchemy.org/en/latest/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat-square&logo=SQLAlchemy)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Uvicorn](https://img.shields.io/badge/-Uvicorn-464646?style=flat-square&logo=uvicorn)](https://www.uvicorn.org/)
[![Gunicorn](https://img.shields.io/badge/-Gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)

### Описание проекта:
Функционал приложение заключается в том, чтобы получать сменные задания (партии) и
уникальные идентификаторы продукции в рамках этой партии,
а так же проверять (по запросу из внешней системы), принадлежит ли данный идентификатор продукции данной партии.

Что умеет приложение:
- Добавления сменных заданий
- Получения сменного задания по ID
- Изменения сменного задания по ID
- Получения списка сменных заданий по фильтрам
- Агрегации продукции
- Базовый CI/CD
- Использование контейнеризацию (docker)
- Покрытие unit, integration тестами

## To Do:
- Добавить больше тестов
- Расширить функционал приложение
- Добавить логирование и вывод ошибок в платформу Sentry

### Инструменты разработки

**Стек:**
- Python >= 3.10
- FastAPI == 0.109.2
- PostgreSQL == 16.1
- Docker == 20.14.24
- Alembic == 1.13.1
- SQLAlchemy == 2.0.26

## Разработка

##### 1) Клонировать репозиторий

    git clone ссылка_сгенерированная_в_вашем_репозитории

##### 2) Установить poetry на компьютер

    https://python-poetry.org/docs/#installation

##### 3) Активировать виртуальное окружение и установить зависимости

        poetry install --no-root

##### 6) Переименовать файл .env.example на .env и изменить на свои данные

##### 7) Установить docker на свою ОС

    https://docs.docker.com/engine/install/

##### 8) Запустить контейнеры через docker

    docker-compose up -d

##### 9) Перейти в документацию api

    127.0.0.1:8000/api/docs


## Дополнительные шаги для запуска CI/CD (прогон тестов, линтеров) и формирование образа в dockerhub:

##### 1) Зарегистрироваться в dockerhub и получить DOCKER_ID (ваш логин в правом углу)

    https://hub.docker.com/

##### 2) Создать access token по инструкции

    https://docs.docker.com/security/for-developers/access-tokens/#create-an-access-token

##### 3) Создать новый репозиторий, перейти в Settings, and go to Secrets and variables > Actions

##### 4) Создать секрет DOCKER_USERNAME с значением DOCKER_ID (выше шагом) и DOCKERHUB_TOKEN с access token

##### 5) Скопировать данный проект в свой созданный репозиторий

##### 6) Сделать push или pull_request в main ветку своего репозитория
    --- Запуститься процесс CI/CD

##### 7) Образом моего проекта, вы можете воспользоваться командой:
    docker pull nikitapython/taskcontrol:latest





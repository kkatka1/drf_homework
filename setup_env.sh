#!/bin/bash

# Удаление старого окружения
rm -rf env

# Создание нового виртуального окружения
python3 -m venv env

# Активация окружения
source env/bin/activate

# Обновление pip и setuptools
python -m ensurepip --upgrade
python -m pip install --upgrade pip setuptools

# Установка зависимостей
pip install -r requirements.txt

echo "Готово: окружение настроено."

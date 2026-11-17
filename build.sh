#!/usr/bin/env bash
# Render build script for InformatikaLab
set -o errexit

pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py collectstatic --noinput

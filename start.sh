#!/bin/bash
#Démarrage de l'application
#zf170420.1512

#python django_example/manage.py runserver

source ./.venv/bin/activate
python src/manage.py runserver 0.0.0.0:8000

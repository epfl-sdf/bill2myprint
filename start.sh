#!/bin/bash
#Démarrage de l'application
#zf170420.1512

#python django_example/manage.py runserver

ssh -fNAL 3306:127.0.0.1:3306 ubuntu@sdf-bill2myprint-mysql-1

source ./.venv/bin/activate
python3 src/manage.py runserver 0.0.0.0:8000

PID=`pgrep -f "ssh -fNAL 3306:127.0.0.1:3306 ubuntu@sdf-bill2myprint-mysql-1"`
if [[ "" !=  "$PID" ]]; then
  echo "killing $PID"
  kill $PID
fi

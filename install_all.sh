#!/bin/bash
#Installation de l'application
#zf170421.1035

./install_python.sh
./acb_uncrypt.sh
./install_mysql.sh
sudo ./install_mssql_driver.sh
./install_django.sh

sudo systemctl stop mysql
sudo systemctl disable mysql

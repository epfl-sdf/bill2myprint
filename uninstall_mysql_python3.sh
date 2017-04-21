#!/bin/bash
#juste on test ;-)
#zf170421.1035

sudo apt-get --purge -y remove mysql-server mysql-common
sudo apt-get --purge -y remove python3 python3-pip

sudo apt-get -y autoremove
sudo apt-get -y clean
sudo apt-get -y autoclean

sudo rm -R /etc/mysql/
sudo rm -R /etc/dbconfig-common/
sudo rm -R /var/lib/mysql
sudo rm /root/.my.cnf

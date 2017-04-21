#!/bin/bash
#Installation de l'application
#zf170421.1035

echo ------------ start install
echo ------------ apt-get update
sudo apt-get update

echo ------------ apt-get install utils
sudo apt-get install -y gnupg2 jq

echo ------------ secrets uncrypt
./acb_uncrypt.sh

echo ------------ apt-get install python3
sudo apt-get install -y python3 python3-pip

echo ------------ install virtualenv
sudo pip3 install virtualenv
virtualenv ./.venv

#!/bin/bash
#Installation de l'application
#zf170502.1711

echo ------------ credentials
DB_ROOT_PASSWORD=`cat ../bill2myprint.secrets.json | jq -r '.DB_ROOT_PASSWORD'`
echo $DB_ROOT_PASSWORD
OUR_DB_PASSWORD=`cat ../bill2myprint.secrets.json | jq -r '.OUR_DB_PASSWORD'`
echo $OUR_DB_PASSWORD

echo ------------ apt-get install mysql
sudo DEBIAN_FRONTEND=noninteractive apt-get -y install mysql-server

echo ------------ mysql_native_password plugin mysql
zSQL=`echo "use mysql;\n"`
zSQL=$zSQL`echo "update user set plugin='mysql_native_password' where User='root';\n"`
zSQL=$zSQL`echo "flush privileges;\n"`
echo -e $zSQL
sudo mysql --user="root" -e "$zSQL"
mysqladmin -u root password $DB_ROOT_PASSWORD
sudo apt-get install -y libmysqlclient-dev

echo ------------ create table build2myprint
source ./.venv/bin/activate
zSQL=`echo "CREATE DATABASE build2myprint;\n"`
zSQL=$zSQL`echo "CREATE USER "build2myprint"@"localhost";\n"`
zSQL=$zSQL`echo "SET password FOR "build2myprint"@"localhost" = password('$OUR_DB_PASSWORD');\n"`
zSQL=$zSQL`echo "GRANT ALL ON build2myprint.* TO "build2myprint"@"localhost";\n"`
echo -e $zSQL
mysql --user="root" --password=$DB_ROOT_PASSWORD -e "$zSQL"

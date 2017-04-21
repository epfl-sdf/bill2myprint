#!/bin/bash
#juste on test ;-)
#zf170420.1112

zPASSWORD=`cat ../django-example.secrets.json | jq -r '.DB_ROOT_PASSWORD'`


echo -e $zPASSWORD

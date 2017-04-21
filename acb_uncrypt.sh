#!/bin/bash
#Décryptage des credentials
#zf170420.1446

ZSECRET="django-example.secrets.json"

gpg2 $ZSECRET.gpg
mv $ZSECRET ../.
rm -R ../.gnupg

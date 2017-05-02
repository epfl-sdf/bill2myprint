#!/bin/bash
#Cryptage des credentials
#zf170502.1653

ZSECRET="bill2myprint.secrets.json"

gpg2 -c ../$ZSECRET
mv ../$ZSECRET.gpg .
rm -R ../.gnupg

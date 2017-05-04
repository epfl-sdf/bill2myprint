#!/bin/bash
#Cryptage des credentials
#zf170420.1446

ZSECRET="bill2myprint.secrets.json"

gpg2 -c ../$ZSECRET
mv ../$ZSECRET.gpg .
rm -R ../.gnupg

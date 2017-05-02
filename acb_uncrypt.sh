#!/bin/bash
#Décryptage des credentials
#zf170502.1654

ZSECRET="bill2myprint.secrets.json"

gpg2 $ZSECRET.gpg
mv $ZSECRET ../.
rm -R ../.gnupg

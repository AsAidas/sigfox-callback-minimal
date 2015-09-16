#! /bin/bash

CERT_NAME=$1

# Generating openssl certificate
openssl genrsa -des3 -out ${CERT_NAME}.key 2048
openssl req -new -key ${CERT_NAME}.key -out ${CERT_NAME}.csr
cp ${CERT_NAME}.key ${CERT_NAME}.key.fr
openssl rsa -in ${CERT_NAME}.key.fr -out ${CERT_NAME}.key
openssl x509 -req -days 365 -in ${CERT_NAME}.csr -signkey ${CERT_NAME}.key -out ${CERT_NAME}.crt

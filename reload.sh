#!/bin/bash
configfile="./credentials.ini"

access_key=`awk '/dns_aliyun_access_key\s*=\s*?(.*)$/{print $3}' $configfile`
secret_key=`awk '/dns_aliyun_access_key_secret\s*=\s*?(.*)$/{print $3}' $configfile`

key_file=/etc/letsencrypt/live/cipherpuzzles.com/privkey.pem
cert_file=/etc/letsencrypt/live/cipherpuzzles.com/fullchain.pem
# copy certificate files to the path specified in the nginx config
cp $cert_file /etc/ssl/cipher-fullchain.crt
cp $key_file /etc/ssl/cipher.key
systemctl reload nginx


# upload certificate files to aliyun CDN
/root/certbot/venv/bin/python3 /root/certbot/uploadcert.py


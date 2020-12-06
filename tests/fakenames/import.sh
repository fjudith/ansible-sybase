#!/bin/bash

set -e

# Install required pakages

if grep -i Ubuntu /etc/os_release
then
    sudo apt-get install -yq \
        build-essential \
        python3-setuptools \
        freetds-bin \
        freetds-dev \
        libct4 \
        libsybdb5 \
        tdsodbc \
        unixodbc \
        unixodbc-dev
elif grep -i CentOS /etc/os-release
then
    sudo yum install -y \
    unixODBC \
    unixODBC-devel \
    freetds \
    freetds-devel

fi

cat << EOF | sudo tee /etc/odbcinst.ini
[FreeTDS]
Description=FreeTDS Driver
Driver=/usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
Setup=/usr/lib/x86_64-linux-gnu/odbc/libtdsS.so
EOF

pip3 install -qr ./test/fakenames/requirements.txt
ls -l /usr/lib/x86_64-linux-gnu/odbc/

python3 ./test/fakenames/import.py --server 172.17.100.51 --filename=test/fakenames/roles/files/10k_fakenames_fra.csv

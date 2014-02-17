#!/bin/sh

rm -rf comar_root

mkdir -p comar_root/var/log
mkdir -p comar_root/var/db

cd ..
cmake .
make
make install DESTDIR=tests/comar_root
cd tests

echo

comar_root/usr/sbin/comar3 --datadir=comar_root/var/db/comar3 --logdir=comar_root/var/log/comar3 --debug --print

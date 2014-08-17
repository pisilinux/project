#!/bin/sh

cd ..
rm -rf command-not-found-$1*

cp -r command-not-found command-not-found-$1

find command-not-found-$1/ -type d -name ".svn" -exec rm -rf '{}' \;

tar cvjf command-not-found-$1.tar.bz2 command-not-found-$1

sha1sum command-not-found-$1.tar.bz2


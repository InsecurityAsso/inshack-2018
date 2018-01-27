#!/usr/bin/env bash

F=files
H=${1}
P=${2}

echo "creating garbage files..."
head -c 3631 /dev/urandom > 1.tmp
head -c 8056 /dev/urandom > 2.tmp
head -c 5058 /dev/urandom > 3.tmp
head -c 4242 /dev/urandom > 4.tmp
echo "sending payload..."
cat 1.tmp $F/logo.png 2.tmp $F/r34dm3.txt 3.tmp $F/dna_decoder 4.tmp $F/flag.txt | nc $H $P
echo "removing garbage files..."
rm -f 1.tmp 2.tmp 3.tmp 4.tmp
echo "done!"

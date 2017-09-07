#!/bin/bash

echo "creating garbage files..."
head -c 3631 /dev/urandom > gb_1.tmp
head -c 8056 /dev/urandom > gb_2.tmp
head -c 5058 /dev/urandom > gb_3.tmp
head -c 2577 /dev/urandom > gb_4.tmp
echo "sending payload..."
cat gb_1.tmp files/logo.png gb_2.tmp files/r34dm3.txt gb_3.tmp files/dna_decoder gb_4.tmp | nc 192.168.56.101 4242
echo "removing garbage files..."
rm -f gb_1.tmp gb_2.tmp gb_3.tmp gb_4.tmp
echo "done!"

CC=gcc
CC_FLAGS=-O3

.PHONY: cipher crypt

all: cipher crypt

cipher: cipher.c
	$(CC) $(CC_FLAGS) -o $@ $<

crypt: cipher.c
	$(CC) $(CC_FLAGS) -DNO_DECRYPTION -o $@ $< 

test: cipher
	head -c 16 /dev/urandom > key.bin
	head cipher.c > cipher.txt
	cp cipher.txt cipher.ref
	./cipher e key.bin cipher.txt
	diff -q cipher.txt cipher.ref ||cat cipher.txt
	echo ""
	./cipher d key.bin cipher.txt
	diff -q cipher.txt cipher.ref &&cat cipher.txt &&echo "TEST PASSED!"
	rm cipher.txt cipher.ref
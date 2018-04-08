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
	diff -q cipher.txt cipher.ref || cat cipher.txt
	echo ""
	./cipher d key.bin cipher.txt
	diff -q cipher.txt cipher.ref && cat cipher.txt && echo "TEST PASSED!"
	rm cipher.txt cipher.ref

chall: crypt
	#head -c 16 /dev/urandom > key.bin
	cat emergency_override.c > emergency_override.enc
	echo -n "//\n// Here is your " >> emergency_override.enc
	echo "$(FLAG)" >> emergency_override.enc
	echo "//" >> emergency_override.enc
	cp emergency_override.enc emergency_override.clear
	./crypt e key.bin emergency_override.enc
	zip stage_3_storage.zip crypt key.bin emergency_override.enc


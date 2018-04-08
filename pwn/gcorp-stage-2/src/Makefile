CC=gcc
CC_FLAGS=-O0 -static

.PHONY: dna_decoder

all: dna_decoder

dna_decoder: dna_decoder.c
	$(CC) $(CC_FLAGS) -o $@ $<

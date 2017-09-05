CC=gcc
CC_FLAGS=-O3

.PHONY: eo

all: eo

eo: emergency_override.c
	$(CC) $(CC_FLAGS) -o $@ $<

CC      ?= gcc
CFLAGS  ?= -std=c11 -Wall -Wextra -Wpedantic -O2

all: build/gradecalc

build/gradecalc: src/gradecalc.c
	@mkdir -p build
	$(CC) $(CFLAGS) -o $@ $<

test: all
	@bash tests/run_tests.sh

clean:
	rm -rf build

.PHONY: all test clean

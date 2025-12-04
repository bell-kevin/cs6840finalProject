CC=gcc
CFLAGS=-std=c11 -Wall -Wextra -pedantic -O2

TARGET=ctl_checker

all: $(TARGET)

$(TARGET): ctl_checker.c
	$(CC) $(CFLAGS) -o $@ $<

clean:
	rm -f $(TARGET)

.PHONY: all clean

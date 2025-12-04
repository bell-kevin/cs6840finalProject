CC=gcc
CFLAGS=-std=c11 -Wall -Wextra -pedantic -O2

TARGET=ctl_checker
TEST_TARGET=ctl_checker_tests

all: $(TARGET)

$(TARGET): ctl_checker.c
	$(CC) $(CFLAGS) -o $@ $<

$(TEST_TARGET): test_ctl_checker.c ctl_checker.c
	$(CC) $(CFLAGS) -DCTL_CHECKER_NO_MAIN -o $@ test_ctl_checker.c

test: $(TEST_TARGET)
	./$(TEST_TARGET)

clean:
	rm -f $(TARGET) $(TEST_TARGET)

.PHONY: all clean test

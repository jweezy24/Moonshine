RM := rm -rf


CFLAGS= -Wall
PYTHON= python3

CC=gcc
LD=ld
SIZE=size


OBJS += \
		main.o\
		


	




all: bin

bin:
	$(CC) $(CFLAGS) src/main.c  -o Moonshine.o

clean:
	rm  Moonshine.o

experiments:
	$(PYTHON) scripts/prepare_python_experiments.py
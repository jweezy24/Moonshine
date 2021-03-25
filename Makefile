RM := rm -rf


ODIR= bin
SDIR= src
CFLAGS= -I src/headers 


CC=gcc
LD=ld
SIZE=size


OBJS += \
		main.o\
		


	

OBJ = $(patsubst %,$(ODIR)/%,$(OBJS))

$(ODIR)/%.o: $(SDIR)/%.c
		$(CC) $(CFLAGS) -c -g -o $@ $^
$(ODIR)/%.o: $(SDIR)/%.s
	nasm -f elf32 -g -o $@ $^

all: bin

bin: $(OBJ)
	$(CC) $(CFLAGS) $(ODIR)/*  -o Moonshine.o

clean:
	rm  Moonshine.o ./bin/main.o

clean_all:
	rm -rf Moonshine bin/*

experiments:
	python3 scripts/prepare_python_experiments.py --data_path '' --NIST_path '' --Moonshine_path ''